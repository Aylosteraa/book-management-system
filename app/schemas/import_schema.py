from pydantic import BaseModel


class ImportResult(BaseModel):
    imported: int
    failed: int
    skipped: int
    errors: list[str]