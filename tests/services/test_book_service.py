import pytest
import src.services.book_service as book_service
from tests.mocks.mock_book_repository import MockBookRepo

def test_get_all_books_positive():
    # AAA - arrange, act, assert
    repo = MockBookRepo()
    svc = book_service.BookService(repo)
    books = svc.get_all_books()
    assert len(books) == 1

def test_find_book_name_negative():
    name = 3
    repo = MockBookRepo()
    svc = book_service.BookService(repo)

    with pytest.raises(TypeError) as e:
        book = svc.find_book_by_name(name)
    assert str(e.value) == 'Expected str, got something else.'


def test_remove_book_positive():
    input_book_id = 'bbb'
    repo = MockBookRepo()
    svc = book_service.BookService(repo)
    book_id = svc.remove_book(input_book_id)
    assert isinstance(book_id, str)

def test_remove_book_negative():
    input_book_id = 1234567
    repo = MockBookRepo()
    svc = book_service.BookService(repo)

    with pytest.raises(TypeError) as e:
        book_id = svc.remove_book(input_book_id)
    assert str(e.value) == 'Expected str, got something else.'


def test_update_book_positive():
    input_book_id = "bbb"
    fields = {"title":"WAS"}

    repo = MockBookRepo()
    svc = book_service.BookService(repo)
    book_id = svc.update_book(input_book_id, fields)
    assert isinstance(book_id, str)

def test_update_book_negative_bad_id():
    input_book_id = 1234567
    fields = {"title":"WAS"}

    repo = MockBookRepo()
    svc = book_service.BookService(repo)

    with pytest.raises(TypeError) as e:
        book_id = svc.update_book(input_book_id, fields)
    assert str(e.value) == 'Expected str, got something else.'

def test_update_book_negative_bad_id():
    input_book_id = "bbb"
    fields = "{\"title\":\"WAS\"}"

    repo = MockBookRepo()
    svc = book_service.BookService(repo)

    with pytest.raises(TypeError) as e:
        book_id = svc.update_book(input_book_id, fields)
    assert str(e.value) == 'Expected a dict, got something else.'
