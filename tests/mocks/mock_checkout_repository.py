from src.domain.checkout_record import CheckoutRecord
from datetime import datetime

class MockCheckoutRepository:
    def __init__(self):
        rec1 = CheckoutRecord(book_id='31907d0a-e1da-4eac-a46e-00b09e7e5fd1', checked_out_at=datetime(2025, 10, 22, 14, 38, 52, 803835), checked_in_at=datetime(2025, 11, 2, 4, 8, 52, 803835), record_id='6ae22de1-57ce-4709-abae-f32541707d53')
        rec2 = CheckoutRecord(book_id='31907d0a-e1da-4eac-a46e-00b09e7e5fd1', checked_out_at=datetime(2025, 12, 2, 14, 38, 52, 803835), checked_in_at=datetime(2026, 1, 2, 4, 8, 52, 803835), record_id='7c54e621-1a2a-5774-ebae-a32de1374d50')
        
        self.records: dict[str, CheckoutRecord] = {rec1.record_id: rec1}

    def add_record(self, record: CheckoutRecord) -> str:
        self.records[record.record_id] = record
        return record.record_id

    def get_active_record_for_book(self, book_id: str):
        if "32r3fe13-de34-2334-cbbe-5432d21707f5" in self.records.keys():
            rec = CheckoutRecord(book_id='31907d0a-e1da-4eac-a46e-00b09e7e5fd1', checked_out_at=datetime(2026, 2, 2, 14, 38, 52, 803835), checked_in_at=None, record_id='32r3fe13-de34-2334-cbbe-5432d21707f5')
            return rec
        else:
            return None

    def get_records_for_book(self, book_id: str) -> list:
        rec1 = CheckoutRecord(book_id='31907d0a-e1da-4eac-a46e-00b09e7e5fd1', checked_out_at=datetime(2025, 10, 22, 14, 38, 52, 803835), checked_in_at=datetime(2025, 11, 2, 4, 8, 52, 803835), record_id='6ae22de1-57ce-4709-abae-f32541707d53')
        rec2 = CheckoutRecord(book_id='31907d0a-e1da-4eac-a46e-00b09e7e5fd1', checked_out_at=datetime(2025, 12, 2, 14, 38, 52, 803835), checked_in_at=datetime(2026, 1, 2, 4, 8, 52, 803835), record_id='7c54e621-1a2a-5774-ebae-a32de1374d50')

        return [
            rec1, rec2
        ]

    def update_record(self, record_id: str, updated_fields: dict) -> str:
        record = self.records[record_id]
        for key, value in updated_fields.items():
            setattr(record, key, value)
        return record_id


    def check_out(self, book_id: str) -> CheckoutRecord:
        rec = CheckoutRecord(book_id='31907d0a-e1da-4eac-a46e-00b09e7e5fd1', checked_out_at=datetime(2026, 2, 2, 14, 38, 52, 803835), checked_in_at=None, record_id='32r3fe13-de34-2334-cbbe-5432d21707f5')
        self.records[rec.record_id] = rec
        return rec

    def check_in(self, book_id: str) -> CheckoutRecord:
        rec = CheckoutRecord(book_id='31907d0a-e1da-4eac-a46e-00b09e7e5fd1', checked_out_at=datetime(2026, 2, 2, 14, 38, 52, 803835), checked_in_at=datetime(2026, 2, 2, 15, 38, 52, 803835), record_id='32r3fe13-de34-2334-cbbe-5432d21707f5')
        self.records[rec.record_id] = rec
        
        return rec