from src.domain.checkout_record import CheckoutRecord

class CheckoutRepository:
    def __init__(self, history = None):
        if history:
            pass
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
        for key, value in updated_fields.items():
            setattr(record, key, value)
        return record_id
    

    def check_out(self, book_id: str) -> CheckoutRecord:
        record = CheckoutRecord(book_id)
        record.check_out()
        self.add_record(record)
        return record

    def check_in(self, book_id: str) -> CheckoutRecord:
        record = self.get_active_record_for_book(book_id)
        record.check_in()
        self.records[record.record_id] = record

        return record
