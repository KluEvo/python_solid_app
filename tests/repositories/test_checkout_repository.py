import pytest
from datetime import datetime

import src.repositories.checkout_repository as checkout_repository
# from src.domain.checkout_record import CheckoutRecord
from tests.mocks.mock_checkout_record import MockCheckoutRecord



@pytest.fixture
def repo(monkeypatch):
    
    monkeypatch.setattr(
        checkout_repository,
        "CheckoutRecord",
        MockCheckoutRecord
    )
    return checkout_repository.CheckoutRepository()


@pytest.fixture
def checked_out_record():
    record = MockCheckoutRecord("book-123")
    record.check_out()
    return record


def test_repository_initializes_with_empty_records():
    repo = checkout_repository.CheckoutRepository()
    assert isinstance(repo.records, dict)
    assert repo.records == {}

def test_repository_initializes_with_history(checked_out_record):
    data = {checked_out_record.record_id:checked_out_record}
    repo = checkout_repository.CheckoutRepository(data)
    assert isinstance(repo.records, dict)
    assert len(repo.records) == 1
    assert checked_out_record.record_id in repo.records 
    assert repo.records[checked_out_record.record_id] == checked_out_record 


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

    repo.update_record(record.record_id, {"checked_in_at": datetime(2025, 12, 1, 3, 22, 52, 803835)})

    assert record.checked_in_at == datetime(2025, 12, 1, 3, 22, 52, 803835)


def test_update_record_add_new_attributes_errors(repo):
    record = repo.check_out("book-123")

    with pytest.raises(Exception):
        repo.update_record(record.record_id, {"custom_field": 42})


def test_update_record_raises_key_error_for_missing_record(repo):
    with pytest.raises(KeyError):
        repo.update_record("nonexistent-id", {"checked_in_at": "x"})


def test_update_record_raises_key_error_for_missing_record(repo):
    record = repo.check_out("book-123")

    with pytest.raises(ValueError):
        repo.update_record(record.record_id, {"checked_in_at": "x"})
    

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
    with pytest.raises(Exception):
        repo.check_in("missing-book")


def test_multiple_active_records_same_book_returns_first_found(repo):
    """
    Theoretically this edge case shouldn't ever happen as we only 
    create a new active record when the last one is closed, but 
    just for safety, we check that multiple active records gives 
    the first one added.
    """
    r1 = MockCheckoutRecord("book-123", datetime(2025, 12, 1, 3, 22, 52, 803835))
    r2 = MockCheckoutRecord("book-123", datetime(2025, 12, 22, 14, 38, 52, 803835))
    r3 = MockCheckoutRecord("book-123", datetime(2026, 11, 4, 14, 38, 52, 803835))

    repo.add_record(r1)
    repo.add_record(r2)
    repo.add_record(r3)

    active = repo.get_active_record_for_book("book-123")

    assert active in (r1, r2, r3)
    assert active.checked_in_at is None
    assert active.checked_out_at == datetime(2025, 12, 1, 3, 22, 52, 803835)
