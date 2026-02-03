from src.domain.book import Book

class MockBookRepo:
    def __init__(self):
        self.__book = Book(title='test', author='author', genre="Mystery", publication_year=2011, page_count=404, average_rating=4.04, ratings_count=40404, price_usd=12.5, publisher="Starlight", language="English", format="Paperback", in_print=True, sales_millions=13, last_checkout=None, available=True, book_id='31907d0a-e1da-4eac-a46e-00b09e7e5fd1')

    def get_all_books(self):
        return [self.__book]
    
    def add_book(self, book):
        return self.__book.book_id
    
    def find_book_by_name(self, query):
        return [self.__book]
    
    def find_book_by_name_and_author(self, title, author):
        return [self.__book]
    
    def find_book_by_id(self, book_id:str) -> Book:
        return self.__book
    
    def remove_book(self, book_id):
        return self.__book.book_id

    def update_book(self, book_id, updated_fields_dict):
        return self.__book.book_id
            
    def check_out_book(self, book_id: str):
        self.__book.available = False
        return True

    def check_in_book(self, book_id: str):
        self.__book.available = True
        return True