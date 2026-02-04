# src/domain/book.py
from dataclasses import dataclass, asdict
from typing import Optional
from dataclasses import dataclass, field
from typing import Optional
import uuid

@dataclass
class MockBook:
    title: str
    author: str
    genre: Optional[int] = None
    publication_year: Optional[int] = None
    page_count: Optional[int] = None
    average_rating: Optional[float] = None
    ratings_count: Optional[int] = None
    price_usd: Optional[float] = None
    publisher: Optional[str] = None
    language: Optional[str] = None
    format: Optional[str] = None
    in_print: Optional[bool] = None
    sales_millions: Optional[float] = None
    last_checkout: Optional[str] = None
    available: Optional[bool] = None
    book_id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

    def check_out(self):
        self.available = False

    def check_in(self):
        self.available = True
