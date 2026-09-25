from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.postgres import SessionLocal
from app.models.schemas.auth import LoginRequest
from app.repositories.UserRepo import UserRepository
from app.services.AuthService import AuthService
from app.models.schemas.signup import SignupRequest
from app.core.security import create_access_token


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


def get_db():
    session = SessionLocal()

    try:
        yield session
    finally:
        session.close()


@router.post("/login")
def login(
    data: LoginRequest,
    session: Session = Depends(get_db),
):

    repository = UserRepository(session)

    service = AuthService(repository)

    user = service.authenticate_user(
        email=data.email,
        password=data.password,
    )

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
        )

    token = create_access_token(user.id)

    return {
        "access_token": token,
        "token_type": "bearer",
    }


@router.post("/signup")
def signup(
    data: SignupRequest,
    session: Session = Depends(get_db),
):

    repository = UserRepository(session)
    service = AuthService(repository)

    user = service.register_user(
        name=data.name,
        email=data.email,
        password=data.password,
    )

    if user is None:
        raise HTTPException(
            status_code=409,
            detail="Email already registered",
        )

    token = create_access_token(user.id)

    return {
        "access_token": token,
        "token_type": "bearer",
    }