# checkout_record.py
from dataclasses import dataclass, field
from datetime import datetime
import uuid

@dataclass
class CheckoutRecord:
    book_id: str
    checked_out_at: datetime | None = None
    checked_in_at: datetime | None = None
    record_id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def check_in(self):
        if self.checked_in_at is not None:
            raise Exception("Book already checked in.")
        self.checked_in_at = datetime.now()

    def check_out(self):
        if self.checked_out_at is not None:
            raise Exception("Book already checked out.")
        self.checked_out_at = datetime.now()
