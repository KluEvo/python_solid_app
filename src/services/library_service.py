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
        elif self.checkout_repo.get_active_record_for_book(book_id):
            raise Exception('Book already checked out.')
        
        self.book_repo.check_out_book(book_id)
                
        
        record = self.checkout_repo.check_out(book_id)

        return record

    def check_in_book(self, book_id: str) -> CheckoutRecord:
        if not isinstance(book_id, str):
            raise TypeError('Expected str, got something else.')
        elif not self.checkout_repo.get_active_record_for_book(book_id):
            raise Exception('Book is has not been checked out.')
        
        self.book_repo.check_in_book(book_id)
        
        record = self.checkout_repo.check_in(book_id)
                
        
        return record
        
    def get_checkout_history(self, book_id: str) -> list[CheckoutRecord]:
        return self.checkout_repo.get_records_for_book(book_id)
