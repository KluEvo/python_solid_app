# library_service.py
from src.domain.book import Book
from src.domain.checkout_record import CheckoutRecord
from src.repositories.book_repository_protocol import BookRepositoryProtocol
from src.repositories.checkout_repository_protocol import CheckoutRepositoryProtocol
from datetime import datetime

class LibraryService:
    def __init__(
        self,
        book_repo: BookRepositoryProtocol,
        checkout_repo: CheckoutRepositoryProtocol,
    ):
        self.book_repo = book_repo
        self.checkout_repo = checkout_repo

    def check_out_book(self, book_id: str) -> CheckoutRecord:
        if not isinstance(book_id, str):
            raise TypeError('Expected str, got something else.')
        
        self.book_repo.check_out_book(book_id)
                
        record = CheckoutRecord(book_id)
        record.check_out()

        
        print(self.book_repo.find_book_by_id(book_id))
        
        self.checkout_repo.add_record(record)

        return record

    def check_in_book(self, book_id: str) -> CheckoutRecord:
        if not isinstance(book_id, str):
            raise TypeError('Expected str, got something else.')
        
        self.book_repo.check_in_book(book_id)
        
        record = CheckoutRecord(book_id=book_id)
        record.check_in()
        
        self.checkout_repo.add_record(record)

        return record
        
    def get_checkout_history(self, book_id: str) -> list[CheckoutRecord]:
        return self.checkout_repo.get_records_for_book(book_id)
