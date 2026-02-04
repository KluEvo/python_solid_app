import pytest
import json
import src.repositories.book_repository as book_repository
from tests.mocks.mock_book_domain import MockBook

@pytest.fixture
def sample_books():
    return [
        MockBook(book_id="1", title="Book 1", author="Author 1", available=True),
        MockBook(book_id="2", title="Book 2", author="Author 2", available=False),
    ]


@pytest.fixture
def mock_json_file(tmp_path, sample_books):
    file = tmp_path / "books.json"
    with open(file, "w") as f:
        json.dump([b.to_dict() for b in sample_books], f)
    return str(file)

def test_get_all_books(monkeypatch, mock_json_file):
    monkeypatch.setattr(
        book_repository,
        "Book",
        MockBook
    )
    repo = book_repository.BookRepository(mock_json_file)
    books = repo.get_all_books()
    print(books)
    assert len(books) == 2
    assert books[0].title == "Book 1"

def test_add_book(monkeypatch, mock_json_file):
    monkeypatch.setattr(
        book_repository,
        "Book",
        MockBook
    )
    repo = book_repository.BookRepository(mock_json_file)
    new_book = MockBook(book_id="3", title="Book 3", author="Author 3", available=True)
    repo.add_book(new_book)
    books = repo.get_all_books()
    assert len(books) == 3
    assert books[2].title == "Book 3"

def test_find_book_by_name(monkeypatch, mock_json_file):
    monkeypatch.setattr(
        book_repository,
        "Book",
        MockBook
    )
    repo = book_repository.BookRepository(mock_json_file)
    result = repo.find_book_by_name("Book 1")
    assert len(result) == 1
    assert result[0].title == "Book 1"

def test_find_book_by_name_and_author(monkeypatch, mock_json_file):
    monkeypatch.setattr(
        book_repository,
        "Book",
        MockBook
    )
    repo = book_repository.BookRepository(mock_json_file)
    result = repo.find_book_by_name_and_author("Book 1", "Author 1")
    assert len(result) == 1
    assert result[0].title == "Book 1"

def test_find_book_by_id(monkeypatch, mock_json_file):
    monkeypatch.setattr(
        book_repository,
        "Book",
        MockBook
    )
    repo = book_repository.BookRepository(mock_json_file)
    result = repo.find_book_by_id("1")
    assert result.title == "Book 1"

def test_find_book_by_id_not_found(monkeypatch, mock_json_file):
    monkeypatch.setattr(
        book_repository,
        "Book",
        MockBook
    )
    repo = book_repository.BookRepository(mock_json_file)
    with pytest.raises(Exception):
        repo.find_book_by_id("99")

def test_remove_book(monkeypatch, mock_json_file):
    monkeypatch.setattr(
        book_repository,
        "Book",
        MockBook
    )
    repo = book_repository.BookRepository(mock_json_file)
    repo.remove_book("1")
    books = repo.get_all_books()
    assert len(books) == 1
    assert books[0].title == "Book 2"

def test_remove_invalid_book(monkeypatch, mock_json_file):
    monkeypatch.setattr(
        book_repository,
        "Book",
        MockBook
    )
    repo = book_repository.BookRepository(mock_json_file)
    with pytest.raises(Exception):
        repo.remove_book("111")
    
def test_update_book(monkeypatch, mock_json_file):
    monkeypatch.setattr(
        book_repository,
        "Book",
        MockBook
    )
    repo = book_repository.BookRepository(mock_json_file)
    repo.update_book("1", {"title": "Updated Book 1"})
    book = repo.find_book_by_id("1")
    assert book.title == "Updated Book 1"

def test_update_book_invalid_field(monkeypatch, mock_json_file):
    monkeypatch.setattr(
        book_repository,
        "Book",
        MockBook
    )
    repo = book_repository.BookRepository(mock_json_file)
    with pytest.raises(ValueError):
        repo.update_book("1", {"does_not_exist": "boom"})

def test_check_out_book(monkeypatch, mock_json_file):
    monkeypatch.setattr(
        book_repository,
        "Book",
        MockBook
    )
    repo = book_repository.BookRepository(mock_json_file)
    availability = repo.check_out_book("1")
    book = repo.find_book_by_id("1")
    assert availability is False
    assert book.available is False

def test_check_in_book(monkeypatch, mock_json_file):
    monkeypatch.setattr(
        book_repository,
        "Book",
        MockBook
    )
    repo = book_repository.BookRepository(mock_json_file)
    availability = repo.check_in_book("2")
    book = repo.find_book_by_id("2")
    assert availability is True
    assert book.available is True

