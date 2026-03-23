from __future__ import annotations

from urllib.parse import urlparse

from app.converter import convert_url_to_pdf_sync


def _is_valid_url(url: str) -> bool:
    parsed = urlparse(url)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def main() -> None:
    print("URL to PDF Interactive Mode")
    print("Enter a URL to convert. Type 'q' to exit.")

    while True:
        user_input = input("\nURL> ").strip()
        if not user_input:
            print("Please enter a URL.")
            continue
        if user_input.lower() in {"q", "quit", "exit"}:
            print("Bye.")
            return
        if not _is_valid_url(user_input):
            print("Invalid URL. Please use http:// or https://")
            continue

        print("Converting, please wait...")
        try:
            pdf_path, title = convert_url_to_pdf_sync(user_input)
            print(f"Done: {pdf_path}")
            if title:
                print(f"Title: {title}")
        except Exception as exc:  # noqa: BLE001
            print(f"Failed: {exc}")
            print("Tip: run 'python -m playwright install chromium' once if not installed.")


if __name__ == "__main__":
    main()
