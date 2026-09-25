from app.core.security import hash_password, verify_password
from app.repositories.UserRepo import UserRepository


class AuthService:

    def __init__(
        self,
        user_repository: UserRepository,
    ):
        self.user_repository = user_repository

    def authenticate_user(
        self,
        email: str,
        password: str,
    ):

        user = self.user_repository.get_by_email(
            email
        )

        if user is None:
            return None

        if not verify_password(
            password,
            user.password,
        ):
            return None

        return user
    def register_user(self, name: str, email: str, password: str):

        existing_user = self.user_repository.get_by_email(email)

        if existing_user is not None:
            return None

        password_hash = hash_password(password)

        return self.user_repository.create_user(
            name=name,
            mail=email,
            password=password_hash
        )