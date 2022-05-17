from pydantic import BaseModel, Field


class ScrapeTarget(BaseModel):
    target: str = Field(...)
