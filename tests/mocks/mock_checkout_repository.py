from src.domain.checkout_record import CheckoutRecord

class FakeCheckoutRepository:
    def __init__(self):
        self.records: dict[str, CheckoutRecord] = {}

    def add_record(self, record: CheckoutRecord) -> str:
        self.records[record.record_id] = record
        return record.record_id

    def get_active_record_for_book(self, book_id: str):
        rec = CheckoutRecord(book_id='31907d0a-e1da-4eac-a46e-00b09e7e5fd1', checked_out_at=datetime.datetime(2026, 2, 2, 14, 38, 52, 803835), checked_in_at=None, record_id='6ae22de1-57ce-4709-abae-f32541707d53')

    def get_records_for_book(self, book_id: str) -> list:
        return [
            r for r in self.records.values()
            if r.book_id == book_id
        ]

    def update_record(self, record_id: str, updated_fields: dict) -> str:
        record = self.records[record_id]
        for key, value in updated_fields.items():
            setattr(record, key, value)
        return record_id
