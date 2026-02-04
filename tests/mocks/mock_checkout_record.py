from dataclasses import dataclass, field
from datetime import datetime
import uuid

@dataclass
class MockCheckoutRecord:
    book_id: str
    checked_out_at: datetime | None = None
    checked_in_at: datetime | None = None
    record_id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def check_in(self):
        self.checked_in_at = datetime.now()

    def check_out(self):
        self.checked_out_at = datetime.now()
