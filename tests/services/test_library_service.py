import pytest
from src.domain.book import Book
from src.services.library_service import LibraryService
import src.services.book_service as book_service
from tests.mocks.mock_book_repository import MockBookRepo
from tests.mocks.mock_checkout_repository import MockCheckoutRepository

@pytest.fixture
def book_repo():
    return MockBookRepo()

@pytest.fixture
def checkout_repo():
    return MockCheckoutRepository()

@pytest.fixture
def library_service(book_repo, checkout_repo):
    return LibraryService(book_repo, checkout_repo)

@pytest.fixture
def sample_book(book_repo):
    book = Book(
        title="test",
        author="author",
        book_id="31907d0a-e1da-4eac-a46e-00b09e7e5fd1",
        available=True,
    )
    book_repo.add_book(book)
    return book

def test_check_out_book_marks_book_unavailable(
    library_service,
    sample_book,
    book_repo,
):
    record = library_service.check_out_book(sample_book.book_id)

    book = book_repo.find_book_by_id(sample_book.book_id)

    assert book.available is False
    assert record.book_id == sample_book.book_id
    assert record.checked_out_at is not None
    assert record.checked_in_at is None


def test_check_out_book_twice_raises_error(
    library_service,
    sample_book,
):
    library_service.check_out_book(sample_book.book_id)

    with pytest.raises(Exception):
        library_service.check_out_book(sample_book.book_id)

def test_check_in_without_active_checkout_raises_error(
    library_service,
    sample_book,
):
    with pytest.raises(Exception):
        library_service.check_in_book(sample_book.book_id)



def test_check_in_book_marks_book_available(
    library_service,
    sample_book,
    book_repo,
    checkout_repo,
):
    record = library_service.check_out_book(sample_book.book_id)

    book = book_repo.find_book_by_id(sample_book.book_id)
    assert book.available is False
    library_service.check_in_book(sample_book.book_id)

    book = book_repo.find_book_by_id(sample_book.book_id)
    updated_record = checkout_repo.records[record.record_id]

    assert book.available is True
    assert updated_record.checked_in_at is not None

def test_get_checkout_history_returns_all_records(
    library_service,
    sample_book,
):

    history = library_service.get_checkout_history(sample_book.book_id)

    assert len(history) == 2
    assert all(r.book_id == sample_book.book_id for r in history)
