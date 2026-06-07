from pydantic import BaseModel


class ImportResult(BaseModel):
    imported: int
    failed: int
    errors: list[str]