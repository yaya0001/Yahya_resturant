from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.database.base import Base

class Branch(Base):
    __tablename__ = "Branches"
    id: Mapped[int]= mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    location:Mapped[str]= mapped_column(String(255), nullable=False)