from sqlalchemy import select
from datetime import datetime
from app.models.database.branch import Branch
from app.models.database.table import Tables as RestaurantTable
from app.models.database.booking import Booking


class BookingRepository:

    def __init__(self, session):
        self.session = session

    def check_availability(
        self,
        date: datetime,
        branch: str,
    ):
        # Find the branch
        branch_obj = self.session.execute(
            select(Branch).where(
                Branch.name == branch
            )
        ).scalar_one_or_none()

        if branch_obj is None:
            return {
                "available": False,
                "reason": "Branch not found",
            }

        # Get all tables in this branch
        tables = self.session.execute(
            select(RestaurantTable).where(
                RestaurantTable.branch_id == branch_obj.id
            )
        ).scalars().all()

        # Get bookings for this date and time
        bookings = self.session.execute(
            select(Booking).where(
                Booking.branch_id == branch_obj.id,
                Booking.booking_time == date,
            )
        ).scalars().all()

        # IDs of tables that are already booked
        booked_table_ids = {
            booking.table_id
            for booking in bookings
        }

        # Tables that are not booked
        available_tables = [
            table
            for table in tables
            if table.id not in booked_table_ids
        ]

        return {
            "available": bool(available_tables),
            "available_tables": [
                {
                    "id": table.id,
                    "capacity": table.capacity,
                }
                for table in available_tables
            ],
            "available_count": len(available_tables),
        }
    def book_table(
        self,
        date: datetime,
        branch: str,
        table_id: int,
        user: int,
    ):
        # Find the branch
        branch_obj = self.session.execute(
            select(Branch).where(
                Branch.name == branch
            )
        ).scalar_one_or_none()

        if branch_obj is None:
            return {
                "success": False,
                "reason": "Branch not found",
            }

        # Check if the table exists in this branch
        table_obj = self.session.execute(
            select(RestaurantTable).where(
                RestaurantTable.id == table_id,
                RestaurantTable.branch_id == branch_obj.id
            )
        ).scalar_one_or_none()

        if table_obj is None:
            return {
                "success": False,
                "reason": "Table not found in this branch",
            }

        # Check if the table is already booked for this date and time
        existing_booking = self.session.execute(
            select(Booking).where(
                Booking.branch_id == branch_obj.id,
                Booking.table_id == table_id,
                Booking.booking_time == date,
            )
        ).scalar_one_or_none()

        if existing_booking:
            return {
                "success": False,
                "reason": "Table already booked for this date and time",
            }

        # Create a new booking
        new_booking = Booking(
            branch_id=branch_obj.id,
            user_id=user,  
            table_id=table_id,
            booking_time=date,
            status="confirmed"
        )

        self.session.add(new_booking)
        self.session.commit()

        return {
            "success": True,
            "booking_id": new_booking.id,
        }
    def cancel_booking(
        self,
        booking_id: int,
    ):
        # Find the booking
        booking_obj = self.session.execute(
            select(Booking).where(
                Booking.id == booking_id
            )
        ).scalar_one_or_none()

        if booking_obj is None:
            return {
                "success": False,
                "reason": "Booking not found",
            }

        # Cancel the booking
        booking_obj.status = "canceled"
        self.session.commit()

        return {
            "success": True,
            "booking_id": booking_id,
        }