from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.database.base import Base

class Booking(Base):
    __tablename__="Booking"
    id: Mapped["int"]=mapped_column(primary_key=True, index=True)
    user_id: Mapped["int"]= mapped_column(ForeignKey("Users.id"),nullable=False)
    branch_id: Mapped["int"]= mapped_column(ForeignKey("Branches.id"), nullable=False)
    table_id: Mapped["int"]= mapped_column(ForeignKey("Tables.id"), nullable=False)
    booking_time: Mapped["DateTime"]= mapped_column(DateTime, nullable=False)
    status: Mapped["str"]= mapped_column(String(255), nullable=False, default="confirmed")