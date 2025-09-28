import datetime
from typing import Optional

from pydantic import BaseModel


# Write your code here
class MovieDetailResponseSchema(BaseModel):
    id: int
    name: str
    date: datetime.date
    score: int
    genre: str
    overview: str
    crew: str
    orig_title: str
    status: str
    orig_lang: str
    budget: float
    revenue: float
    country: str

    class Config:
        from_attributes = True


class MovieListResponseSchema(BaseModel):
    movies: list[MovieDetailResponseSchema]
    prev_page: Optional[str]
    next_page: Optional[str]
    total_items: int
    total_pages: int
