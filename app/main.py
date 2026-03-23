from fastapi import FastAPI, HTTPException
from fastapi.concurrency import run_in_threadpool

from app import __version__
from app.converter import convert_url_to_pdf_sync
from app.models import ConvertRequest, ConvertResponse


app = FastAPI(title="URL to PDF for AI Reading", version=__version__)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/convert", response_model=ConvertResponse)
async def convert(request: ConvertRequest) -> ConvertResponse:
    try:
        pdf_path, title = await run_in_threadpool(
            convert_url_to_pdf_sync,
            str(request.url),
            request.wait_until,
            request.timeout_ms,
        )
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=f"convert failed: {exc}") from exc

    return ConvertResponse(source_url=str(request.url), pdf_path=pdf_path, title=title)
