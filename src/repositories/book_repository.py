import json
from src.domain.book import Book
from src.repositories.book_repository_protocol import BookRepositoryProtocol
from typing import get_type_hints

class BookRepository(BookRepositoryProtocol):
    def __init__(self, filepath: str="books.json"):
        self.filepath = filepath

    def get_all_books(self) -> list[Book]:
        with open(self.filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return [Book.from_dict(item) for item in data]

    def add_book(self, book:Book) -> str:
        books = self.get_all_books()
        books.append(book)
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump([b.to_dict() for b in books], f, indent=2)
        return book.book_id

    def find_book_by_name(self, query) -> Book:
        return [b for b in self.get_all_books() if b.title == query]
    

    def find_book_by_name_and_author(self, title:str, author:str) -> list[Book]:
        return [b for b in self.get_all_books() if b.title == title and b.author == author]
    
    def find_book_by_id(self, book_id:str) -> Book:
        books = [b for b in self.get_all_books() if b.book_id == book_id]
        if books:
            return books[0]
        else:
            raise Exception(f"No book with id {book_id}")
    

    def __find_exact_book(self, attributes:dict = None):
        # TODO: implement finding books by attribute     
        pass

    # to be turned into remove book
    def remove_book(self, book_id:str) -> str:
        
        books = self.get_all_books()

        book = self.find_book_by_id(book_id) 

        books.remove(book)

        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump([b.to_dict() for b in books], f, indent=2)
        return book.book_id

    # to be turned into edit book
    def update_book(self, book_id:str, updated_fields_dict:dict) -> str:
        books = self.get_all_books()

        book = self.find_book_by_id(book_id)


        books.remove(book)
        book_dict = book.to_dict()

        type_hints = get_type_hints(book)
        for field_name, value in updated_fields_dict.items():
            if field_name not in type_hints:
                raise ValueError(f"Field '{field_name}' does not exist in Book.")

            expected_type = type_hints[field_name]
            origin_type = getattr(expected_type, "__origin__", expected_type)

            if value is None and origin_type is not None and hasattr(origin_type, "__args__"):
                origin_type = origin_type.__args__[0]

            try:
                if origin_type == int:
                    book_dict[field_name] = int(value)
                elif origin_type == float:
                    book_dict[field_name] = float(value)
                elif origin_type == bool:
                    book_dict[field_name] = bool(value)
                elif origin_type == str:
                    book_dict[field_name] = str(value)
                else:
                    book_dict[field_name] = value
            except (ValueError, TypeError) as e:
                raise ValueError(f"Updated contents of field '{field_name}' does not match field typing: {e}")


        print(book_dict)
        book = Book.from_dict(book_dict)

        print(4)
        books.append(book)
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump([b.to_dict() for b in books], f, indent=2)
        return book.book_id


    def check_out_book(self, book_id: str) -> bool:
        book = self.find_book_by_id(book_id)
        book.check_out()
        return book.available == False

    def check_in_book(self, book_id: str) -> bool:
        book = self.find_book_by_id(book_id)
        book.check_in()
        return book.available == True

    # def find_exact_book(self, title:str, author:str):
    #     books = self.find_book_by_name_and_author(title, author)
    #     if len(books) > 1:
    #         print("Multiple books with the same author and title:")
    #         for i in range(len(books)):
    #             print(f"{i+1}. {books[i]}")
    #         book_selection = int(input("Which book to remove? Enter the number: "))
    #         book_target = books[book_selection -1]
    #     elif len(books == 0):
    #         if not isinstance(title, str):
    #             raise TypeError('Expected str, got something else.')
    #     else:
    #         book_target = books[0]

    #     return book_target

    # # to be turned into remove book
    # def remove_book(self, title:str, author:str) -> str:
        
    #     book = self.find_exact_book(title, author)
    
    #     books = self.get_all_books()

    #     books.remove(book)

    #     with open(self.filepath, 'w', encoding='utf-8') as f:
    #         json.dump([b.to_dict() for b in books], f, indent=2)
    #     return book.book_id

    # # to be turned into edit book
    # def update_book(self, title:str, author:str, updated_fields_dict:dict) -> str:
    #     book_to_update = self.find_exact_book(title, author)

    #     books = self.get_all_books()

    #     books.remove(book_to_update)

    #     boot_dict = book.to_dict()

    #     for key in updated_fields_dict:
    #         boot_dict[key] = updated_fields_dict[key]

    #     book = Book.from_dict(book_to_update)

    #     books.append(book)
    #     with open(self.filepath, 'w', encoding='utf-8') as f:
    #         json.dump([b.to_dict() for b in books], f, indent=2)
    #     return book_to_update[0].book_id

