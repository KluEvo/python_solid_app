from typing import Protocol
from src.domain.book import Book

class BookRepositoryProtocol(Protocol):
    def get_all_books(self) -> list[Book]:
        ...

    def add_book(self, book:Book) -> str:
        ...

    def find_book_by_name(self, query:str) -> list[Book]:
        ...

    def find_book_by_name_and_author(self, title:str, author:str) -> list[Book]:
        ...

    def find_book_by_id(self, book_id:str) -> Book:
        ...
        
    def remove_book(self, book_id:str) -> str:
        ...

    def update_book(self, book_id:str, updated_fields_dict:dict) -> str:
        ...

        
    def check_out_book(self, book_id: str) -> bool:
        ...

    def check_in_book(self, book_id: str) -> bool:
        ...