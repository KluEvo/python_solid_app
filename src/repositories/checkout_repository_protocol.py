from typing import Protocol, List
from src.domain.checkout_record import CheckoutRecord

class CheckoutRepositoryProtocol(Protocol):

    def add_record(self, record: CheckoutRecord) -> str:
        ...

    def get_records_for_book(self, book_id: str) -> List[CheckoutRecord]:
        ...

    def update_record(self, record_id: str, updated_fields: dict) -> str:
        ...
