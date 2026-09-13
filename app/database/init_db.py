from app.database.postgres import engine
from app.models.database import Base


def init_db() -> None:
    Base.metadata.create_all(bind=engine)