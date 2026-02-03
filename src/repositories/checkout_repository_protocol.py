from typing import Protocol, List
from src.domain.checkout_record import CheckoutRecord

class CheckoutRepositoryProtocol(Protocol):

    def add_record(self, record: CheckoutRecord) -> str:
        ...

    def get_records_for_book(self, book_id: str) -> List[CheckoutRecord]:
        ...

    def get_active_record_for_book(self, book_id: str):
        ...

    def get_records_for_book(self, book_id: str) -> list:
        ...

    def update_record(self, record_id: str, updated_fields: dict) -> str:
        ...

    def check_out(self, book_id: str) -> CheckoutRecord:
        ...

    def check_in(self, book_id: str) -> CheckoutRecord:
        ...