from src.repositories.book_repository_protocol import BookRepositoryProtocol
from src.domain.book import Book

class BookService:
    def __init__(self, repo: BookRepositoryProtocol):
        self.repo = repo

    def get_all_books(self) -> list[Book]:
        return self.repo.get_all_books()

    def add_book(self, book:Book) -> str:
        return self.repo.add_book(book)

    def find_book_by_name(self, query:str) -> list[Book]:
        if not isinstance(query, str):
            raise TypeError('Expected str, got something else.')
        return self.repo.find_book_by_name(query)
    
    def find_book_by_name_and_author(self, title:str, author:str) -> list[Book]:
        if not isinstance(title, str):
            raise TypeError('Expected str, got something else.')
        if not isinstance(author, str):
            raise TypeError('Expected str, got something else.')
        return self.repo.find_book_by_name_and_author(title, author)

    def remove_book(self, book_id:str) -> str:
        if not isinstance(book_id, str):
            raise TypeError('Expected str, got something else.')
        return self.repo.remove_book(book_id)

    def update_book(self, book_id:str, updated_fields_dict:dict) -> str:
        if not isinstance(book_id, str):
            raise TypeError('Expected str, got something else.')
        if not isinstance(updated_fields_dict, dict):
            raise TypeError('Expected a dict, got something else.')
        return self.repo.update_book(book_id, updated_fields_dict)

    def find_book_by_id(self, book_id:str) -> str:
        return self.repo.find_book_by_id(book_id)
