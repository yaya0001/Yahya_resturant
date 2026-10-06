import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import create_access_token
from app.database.postgres import SessionLocal
from app.models.schemas.auth import LoginRequest
from app.models.schemas.signup import SignupRequest
from app.repositories.UserRepo import UserRepository
from app.services.AuthService import AuthService


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

security = HTTPBearer(auto_error=False)


@router.get("", include_in_schema=False)
@router.get("/", include_in_schema=False)
def auth_root():
    return {
        "message": "Authentication endpoints",
        "endpoints": [
            "/auth/login",
            "/auth/signup",
            "/auth/me",
        ],
    }


def get_db():
    session = SessionLocal()

    try:
        yield session
    finally:
        session.close()


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
    session: Session = Depends(get_db),
):
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing bearer token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        token = credentials.credentials
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
        )
        user_id = int(payload.get("sub"))
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc

    user = UserRepository(session).get_by_id(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


def get_current_user_id(
    current_user=Depends(get_current_user),
) -> int:
    return current_user.id


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


@router.get("/me")
def get_me(
    current_user=Depends(get_current_user),
):
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.mail,
    }