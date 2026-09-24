from datetime import datetime
class AvailabilityService:
    def __init__(self, repository):
        self.repository = repository

    def check(
        self,
        date: datetime,
        branch: str,
    ):
        return self.repository.check_availability(
            date=date,
            branch=branch,
        )
    def book(
        self,
        date: datetime,
        branch: str,
        table_id: int,
        user: int,
    ):
        return self.repository.book_table(
            date=date,
            branch=branch,
            table_id=table_id,
            user=user,
        )
    def cancel(
        self,
        booking_id: int,
    ):
        return self.repository.cancel_booking(
            booking_id=booking_id,
        )