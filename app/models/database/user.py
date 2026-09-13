from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.database.base import Base

class Users(Base):
    __tablename__="Users"
    id: Mapped[int]=mapped_column(primary_key=True, index=True)
    name: Mapped[str]=mapped_column(String(255), nullable=False)
    mail: Mapped[str]= mapped_column(String(255), nullable=False, unique=True)
    password: Mapped[str]= mapped_column(String(255), nullable=False)