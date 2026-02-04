import pytest

from src.repositories.checkout_repository import CheckoutRepository
from src.domain.checkout_record import CheckoutRecord
from tests.mocks.mock_checkout_record import MockCheckoutRecord



@pytest.fixture
def repo():
    return CheckoutRepository()


@pytest.fixture
def checked_out_record():
    record = CheckoutRecord("book-123")
    record.check_out()
    return record


def test_repository_initializes_with_empty_records():
    repo = CheckoutRepository()
    assert isinstance(repo.records, dict)
    assert repo.records == {}


def test_add_record_stores_and_returns_record_id(repo, checked_out_record):
    record_id = repo.add_record(checked_out_record)

    assert record_id == checked_out_record.record_id
    assert record_id in repo.records
    assert repo.records[record_id] is checked_out_record


def test_get_active_record_for_book_returns_active_record(repo):
    record = repo.check_out("book-123")

    active = repo.get_active_record_for_book("book-123")

    assert active is record
    assert active.checked_in_at is None


def test_get_active_record_for_book_returns_none_if_no_records(repo):
    assert repo.get_active_record_for_book("missing-book") is None


def test_get_active_record_for_book_returns_none_if_all_checked_in(repo):
    record = repo.check_out("book-123")
    repo.check_in("book-123")

    active = repo.get_active_record_for_book("book-123")

    assert active is None


def test_get_records_for_book_returns_all_records_for_book(repo):
    r1 = repo.check_out("book-123")
    repo.check_in("book-123")
    r2 = repo.check_out("book-123")
    r3 = repo.check_out("other-book")

    records = repo.get_records_for_book("book-123")

    assert r1 in records
    assert r2 in records
    assert r3 not in records
    assert len(records) == 2


def test_get_records_for_book_returns_empty_list_when_none_exist(repo):
    records = repo.get_records_for_book("missing-book")

    assert records == []


def test_update_record_updates_existing_fields(repo):
    record = repo.check_out("book-123")

    repo.update_record(record.record_id, {"checked_in_at": "some-timestamp"})

    assert record.checked_in_at == "some-timestamp"


def test_update_record_can_add_new_attributes(repo):
    record = repo.check_out("book-123")

    repo.update_record(record.record_id, {"custom_field": 42})

    assert hasattr(record, "custom_field")
    assert record.custom_field == 42


def test_update_record_raises_key_error_for_missing_record(repo):
    with pytest.raises(KeyError):
        repo.update_record("nonexistent-id", {"checked_in_at": "x"})


def test_check_out_creates_and_stores_active_record(repo):
    record = repo.check_out("book-123")

    assert record.book_id == "book-123"
    assert record.checked_in_at is None
    assert record.record_id in repo.records


def test_check_in_checks_in_active_record(repo):
    record = repo.check_out("book-123")

    checked_in = repo.check_in("book-123")

    assert checked_in is record
    assert checked_in.checked_in_at is not None
    assert repo.records[record.record_id] is record


def test_check_in_raises_error_if_no_active_record_exists(repo):
    """
    Current behavior: get_active_record_for_book returns None,
    and calling check_in() on None raises AttributeError.
    This test documents that behavior.
    """
    with pytest.raises(AttributeError):
        repo.check_in("missing-book")


def test_multiple_active_records_same_book_returns_first_found(repo):
    """
    Edge case: repository allows multiple active records for the same book.
    get_active_record_for_book returns the first one it encounters.
    """
    r1 = CheckoutRecord("book-123")
    r1.check_out()
    r2 = CheckoutRecord("book-123")
    r2.check_out()

    repo.add_record(r1)
    repo.add_record(r2)

    active = repo.get_active_record_for_book("book-123")

    assert active in (r1, r2)
    assert active.checked_in_at is None
