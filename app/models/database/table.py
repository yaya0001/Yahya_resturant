from sqlalchemy import integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.models.database.base import Base

class Tables(Base):
    __tablename__="Tables"
    id: Mapped["int"]=mapped_column(primary_key=True, index=True)
    branch_id: Mapped["int"]= mapped_column(ForeignKey("Branches.id"), nullable=False)
    capacity: Mapped["int"]= mapped_column(integer, nullable=False)
    is_available: Mapped["bool"]= mapped_column(nullable=False, default=True)