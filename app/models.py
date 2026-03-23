from pydantic import BaseModel, HttpUrl


class ConvertRequest(BaseModel):
    url: HttpUrl
    wait_until: str = "networkidle"
    timeout_ms: int = 90000


class ConvertResponse(BaseModel):
    source_url: str
    pdf_path: str
    title: str | None = None
