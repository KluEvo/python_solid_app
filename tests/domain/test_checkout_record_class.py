from datetime import datetime
import pytest

from src.domain.checkout_record import CheckoutRecord, CheckoutError


def test_checkout_record_initial_state():
    record = CheckoutRecord(book_id="book-123")

    assert record.book_id == "book-123"
    assert record.checked_out_at is None
    assert record.checked_in_at is None
    assert record.record_id is not None
    assert isinstance(record.record_id, str)


def test_check_out_sets_checked_out_at():
    record = CheckoutRecord(book_id="book-123")

    record.check_out()

    assert record.checked_out_at is not None
    assert isinstance(record.checked_out_at, datetime)
    assert record.checked_in_at is None


def test_check_out_raises_if_already_checked_out():
    record = CheckoutRecord(book_id="book-123")
    record.check_out()

    with pytest.raises(CheckoutError, match="Book already checked out."):
        record.check_out()


def test_check_in_sets_checked_in_at():
    record = CheckoutRecord(book_id="book-123")

    record.check_in()

    assert record.checked_in_at is not None
    assert isinstance(record.checked_in_at, datetime)


def test_check_in_raises_if_already_checked_in():
    record = CheckoutRecord(book_id="book-123")
    record.check_in()

    with pytest.raises(CheckoutError, match="Book already checked in."):
        record.check_in()


def test_check_out_and_check_in_flow():
    record = CheckoutRecord(book_id="book-123")

    record.check_out()
    record.check_in()

    assert record.checked_out_at is not None
    assert record.checked_in_at is not None
    assert record.checked_in_at >= record.checked_out_at
