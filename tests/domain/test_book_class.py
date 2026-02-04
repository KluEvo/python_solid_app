import pytest
import uuid
from dataclasses import asdict
from datetime import datetime
from src.domain.book import Book, BookError

def test_book_creation_with_required_fields():
    book = Book(title="Test", author="Arthur Scribe")
    assert book.title == "Test"
    assert book.author == "Arthur Scribe"
    assert isinstance(book.book_id, str)
    assert len(book.book_id) > 0

def test_book_creation_with_all_fields():
    book = Book(
        title="Test",
        author="Arthur Scribe",
        genre=1,
        publication_year=2000,
        page_count=310,
        average_rating=4.5,
        ratings_count=1000000,
        price_usd=12.99,
        publisher="Papers",
        language="English",
        format="Hardcover",
        in_print=True,
        sales_millions=100.0,
        last_checkout="2023-01-01",
        available=True
    )
    assert book.title == "Test"
    assert book.genre == 1
    assert book.publication_year == 2000
    assert book.available is True

def test_book_creation_with_none_optional_fields():
    book = Book(title="Test", author="Arthur Scribe")
    assert book.genre is None
    assert book.publication_year is None
    assert book.available is None

def test_book_id_is_unique():
    book1 = Book(title="Test", author="Arthur Scribe")
    book2 = Book(title="Test", author="Arthur Scribe")
    assert book1.book_id != book2.book_id

def test_check_out_success():
    book = Book(title="Test", author="Arthur Scribe", available=True)
    book.check_out()
    assert book.available is False

def test_check_out_failure():
    book = Book(title="Test", author="Arthur Scribe", available=False)
    with pytest.raises(BookError, match="Book is already checked out."):
        book.check_out()

def test_check_in_success():
    book = Book(title="Test", author="Arthur Scribe", available=False)
    book.check_in()
    assert book.available is True

def test_check_in_failure():
    book = Book(title="Test", author="Arthur Scribe", available=True)
    with pytest.raises(BookError, match="Book is already available."):
        book.check_in()

def test_from_dict():
    data = {
        "title": "Test",
        "author": "Arthur Scribe",
        "genre": 1,
        "publication_year": 2000,
        "available": True
    }
    book = Book.from_dict(data)
    assert book.title == "Test"
    assert book.genre == 1
    assert book.available is True

def test_to_dict():
    book = Book(
        title="Test",
        author="Arthur Scribe",
        genre=1,
        publication_year=2000,
        available=True
    )
    data = book.to_dict()
    assert data["title"] == "Test"
    assert data["genre"] == 1
    assert data["available"] is True
    assert "book_id" in data

def test_to_dict_matches_asdict():
    book = Book(
        title="Test",
        author="Arthur Scribe",
        genre=1,
        publication_year=2000,
        available=True
    )
    assert book.to_dict() == asdict(book)
