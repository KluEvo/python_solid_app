from src.domain.book import Book

class MockBookRepo:
    def get_all_books(self):
        return [Book(title="test", author="author")]
    
    def add_book(self, book):
        return 'mock_id'
    
    def find_book_by_name(self, query):
        return [Book(title="test", author="author")]

    
    def find_book_by_name_and_author(self, title, author):
        return [Book(title="test", author="author")]

    def find_book_by_id(self, book_id:str) -> Book:
        return Book(title="test", author="author")

    def remove_book(self, book_id):
        return 'mock_id'

    def update_book(self, book_id, updated_fields_dict):
        return 'mock_id'
    
    
        
    def check_out_book(self, book_id: str):
        return True

    def check_in_book(self, book_id: str):
        return True