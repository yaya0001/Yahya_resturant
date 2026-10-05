from datetime import datetime

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database.postgres import SessionLocal
from app.repositories.booking_repository import BookingRepository
from app.services.booking_service import AvailabilityService


class AvailabilityRequest(BaseModel):
    date: datetime
    branch: str


class BookingRequest(BaseModel):
    date: datetime
    branch: str
    table_id: int
    user: int


class CancelBookingRequest(BaseModel):
    booking_id: int


router = APIRouter(
    prefix="/booking",
    tags=["Booking"],
)


def get_db():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@router.post("/availability")
def check_availability(
    payload: AvailabilityRequest,
    session: Session = Depends(get_db),
):
    service = AvailabilityService(BookingRepository(session))
    return service.check(
        date=payload.date,
        branch=payload.branch,
    )


@router.post("/book")
def book_table(
    payload: BookingRequest,
    session: Session = Depends(get_db),
):
    service = AvailabilityService(BookingRepository(session))
    return service.book(
        date=payload.date,
        branch=payload.branch,
        table_id=payload.table_id,
        user=payload.user,
    )


@router.post("/cancel")
def cancel_booking(
    payload: CancelBookingRequest,
    session: Session = Depends(get_db),
):
    service = AvailabilityService(BookingRepository(session))
    return service.cancel(
        booking_id=payload.booking_id,
    )
