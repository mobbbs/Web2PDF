# URL to PDF for AI Reading

Convert a web page URL into an AI-friendly PDF.

## Features

- FastAPI API endpoint: `POST /convert`
- Playwright page rendering for JS-heavy sites
- Readability-based main-content extraction
- A4 PDF output with page numbers

## Quick Start

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m playwright install chromium
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## API Example

```powershell
curl -X POST "http://127.0.0.1:8000/convert" `
  -H "Content-Type: application/json" `
  -d "{\"url\":\"https://learnopengl-cn.github.io/05%20Advanced%20Lighting/06%20HDR/\"}"
```

Response example:

```json
{
  "source_url": "https://learnopengl-cn.github.io/05%20Advanced%20Lighting/06%20HDR/",
  "pdf_path": "Z:\\mobbb\\tools\\output\\learnopengl-cn.github.io_60b6ea085108.pdf",
  "title": "HDR - LearnOpenGL CN"
}
```

## Local Packaging

Build release artifacts locally:

```powershell
pip install build
python -m build
```

Output:

- `dist/*.whl`
- `dist/*.tar.gz`

## GitHub Release Automation

This repo includes workflow: `.github/workflows/release.yml`

Trigger rule:

- Push a tag in format `vX.Y.Z`

Workflow will:

- Build `sdist` and `wheel`
- Create a source zip
- Create GitHub Release
- Upload build artifacts to the Release page

## Release Command (PowerShell)

Prepare version commit + tag:

```powershell
.\scripts\release.ps1 -Version 0.1.1
```

Then publish:

```powershell
git push origin HEAD --tags
```

After push, GitHub Actions creates the Release automatically.
