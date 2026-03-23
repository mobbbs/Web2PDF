import asyncio
import hashlib
import re
from pathlib import Path
from urllib.parse import urlparse

from bs4 import BeautifulSoup
from playwright.async_api import TimeoutError as PlaywrightTimeoutError
from playwright.async_api import async_playwright
from readability import Document


OUTPUT_DIR = Path("output")


def _safe_filename(text: str, fallback: str = "document") -> str:
    cleaned = re.sub(r"[^\w\-\. ]+", "", text, flags=re.UNICODE).strip()
    cleaned = re.sub(r"\s+", "_", cleaned)
    return cleaned[:80] or fallback


def _url_hash(url: str) -> str:
    return hashlib.sha256(url.encode("utf-8")).hexdigest()[:12]


def _extract_article_html(raw_html: str) -> tuple[str, str | None]:
    doc = Document(raw_html)
    title = doc.short_title()
    article_html = doc.summary(html_partial=True)
    soup = BeautifulSoup(article_html, "lxml")
    return str(soup), title


def _build_print_html(base_url: str, title: str | None, article_html: str) -> str:
    escaped_title = BeautifulSoup(title or "Untitled", "lxml").text
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <base href="{base_url}" />
  <title>{escaped_title}</title>
  <style>
    @page {{
      size: A4;
      margin: 18mm 14mm 18mm 14mm;
    }}
    body {{
      font-family: "Noto Sans SC", "PingFang SC", "Microsoft YaHei", sans-serif;
      line-height: 1.7;
      color: #101828;
      font-size: 14px;
      word-break: break-word;
    }}
    h1, h2, h3, h4 {{
      color: #111827;
      margin-top: 1.2em;
      margin-bottom: 0.5em;
      page-break-after: avoid;
    }}
    p {{
      margin: 0.55em 0;
    }}
    pre, code {{
      font-family: Consolas, "Cascadia Mono", monospace;
      white-space: pre-wrap;
      word-break: break-word;
    }}
    pre {{
      background: #f7f8fa;
      border: 1px solid #e5e7eb;
      border-radius: 8px;
      padding: 10px 12px;
      overflow: hidden;
    }}
    img {{
      max-width: 100%;
      height: auto;
      page-break-inside: avoid;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      margin: 0.8em 0;
      font-size: 12px;
    }}
    th, td {{
      border: 1px solid #d0d5dd;
      padding: 6px 8px;
      vertical-align: top;
    }}
    a {{
      color: #175cd3;
      text-decoration: none;
    }}
    blockquote {{
      border-left: 3px solid #98a2b3;
      margin: 0.8em 0;
      padding: 0.4em 0.9em;
      color: #344054;
      background: #f8fafc;
    }}
  </style>
</head>
<body>
  <h1>{escaped_title}</h1>
  {article_html}
</body>
</html>
"""


async def convert_url_to_pdf(
    url: str,
    wait_until: str = "networkidle",
    timeout_ms: int = 90000,
) -> tuple[str, str | None]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    parsed = urlparse(url)
    slug = _safe_filename(parsed.path.split("/")[-1] or parsed.netloc, "page")
    file_name = f"{slug}_{_url_hash(url)}.pdf"
    output_path = OUTPUT_DIR / file_name

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        try:
            page = await browser.new_page()
            try:
                await page.goto(url, wait_until=wait_until, timeout=timeout_ms)
            except PlaywrightTimeoutError:
                await page.goto(url, wait_until="domcontentloaded", timeout=timeout_ms)

            raw_html = await page.content()
            article_html, title = _extract_article_html(raw_html)
            print_html = _build_print_html(url, title, article_html)

            printer = await browser.new_page()
            await printer.set_content(print_html, wait_until="networkidle", timeout=timeout_ms)
            await printer.pdf(
                path=str(output_path),
                format="A4",
                print_background=True,
                display_header_footer=True,
                header_template="<span></span>",
                footer_template=(
                    "<div style='font-size:8px;width:100%;padding:0 12px;color:#667085;'>"
                    "<span class='pageNumber'></span>/<span class='totalPages'></span>"
                    "</div>"
                ),
                margin={"top": "14mm", "bottom": "14mm", "left": "10mm", "right": "10mm"},
            )
            await printer.close()
        finally:
            await browser.close()

    return str(output_path.resolve()), title


def convert_url_to_pdf_sync(
    url: str,
    wait_until: str = "networkidle",
    timeout_ms: int = 90000,
) -> tuple[str, str | None]:
    return asyncio.run(convert_url_to_pdf(url=url, wait_until=wait_until, timeout_ms=timeout_ms))
