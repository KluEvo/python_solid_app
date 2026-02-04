from src.domain.checkout_record import CheckoutRecord
from typing import get_type_hints
from datetime import datetime

class CheckoutRepository:
    def __init__(self, history = None):
        if history:
            self.records = history
        else:
            self.records: dict[str, CheckoutRecord] = {}

    def add_record(self, record: CheckoutRecord) -> str:
        self.records[record.record_id] = record
        return record.record_id

    def get_active_record_for_book(self, book_id: str):
        for record in self.records.values():
            if record.book_id == book_id and record.checked_in_at is None:
                return record
        return None

    def get_records_for_book(self, book_id: str) -> list:
        return [r for r in self.records.values() if r.book_id == book_id]

    def update_record(self, record_id: str, updated_fields: dict) -> str:
        record = self.records[record_id]
        type_hints = get_type_hints(CheckoutRecord)
        for field_name, value in updated_fields.items():
            if field_name not in type_hints:
                raise ValueError(f"Field '{field_name}' does not exist in CheckoutRecord.")
            
            
            expected_type = type_hints[field_name]
            origin_type = getattr(expected_type, "__origin__", expected_type)

            if value is None and origin_type is not None and hasattr(origin_type, "__args__"):
                origin_type = origin_type.__args__[0]

            if (field_name == "checked_in_at" or field_name == "checked_out_at") and type(value) != datetime:
                raise ValueError(f"Field '{field_name}' shoulde be a datetime object.")

            try:
                if origin_type == str:
                    setattr(record, field_name, str(value))
            except (ValueError, TypeError) as e:
                raise ValueError(f"Updated contents of field '{field_name}' does not match field typing: {e}")

        return record_id
    

    def check_out(self, book_id: str) -> CheckoutRecord:
        record = CheckoutRecord(book_id)
        
        record.check_out()
        self.add_record(record)
        return record

    def check_in(self, book_id: str) -> CheckoutRecord:
        record = self.get_active_record_for_book(book_id)
        
        if record:
            record.check_in()
            self.records[record.record_id] = record

            return record
        else:
            raise Exception(f"No book with book id {book_id}")
        
