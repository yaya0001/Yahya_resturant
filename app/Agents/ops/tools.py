from typing import Annotated

from langchain_core.tools import tool
from langgraph.prebuilt import InjectedState

from app.database.postgres import SessionLocal
from app.repositories.booking_repository import BookingRepository
from app.services.booking_service import AvailabilityService
from datetime import datetime
@tool
def check_table_availability(
    date: datetime,
    branch: str,
) -> dict:
    """
    Check whether a restaurant table is available
    for a specific date, time, and branch.
    """

    session = SessionLocal()

    try:
        repository = BookingRepository(session)

        service = AvailabilityService(repository)

        return service.check(
            date=date,
            branch=branch,
        )

    finally:
        session.close()


@tool
def book_table(
    date: datetime,
    branch: str,
    table_id: int,
    user_id: Annotated[str, InjectedState("user_id")],
) -> dict:
    """
    Book a restaurant table for a specific date, time, and branch.
    The authenticated user ID is provided by the chat state.
    """

    session = SessionLocal()

    try:
        repository = BookingRepository(session)

        service = AvailabilityService(repository)

        return service.book(
            date=date,
            branch=branch,
            table_id=table_id,
            user=int(user_id),
        )

    finally:
        session.close()

@tool
def cancel_booking(
    booking_id: int,
) -> dict:
    """
    Cancel a restaurant table booking by its ID.
    """

    session = SessionLocal()

    try:
        repository = BookingRepository(session)

        return repository.cancel_booking(booking_id)

    finally:
        session.close()
