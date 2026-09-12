from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings


DATABASE_URL = (
    f"postgresql+psycopg://"
    f"{settings.postgres_user}:"
    f"{settings.postgres_password}@"
    f"{settings.postgres_host}:"
    f"{settings.postgres_port}/"
    f"{settings.postgres_db}"
)


engine = create_engine(
    DATABASE_URL,
    echo=settings.debug,
)


SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)