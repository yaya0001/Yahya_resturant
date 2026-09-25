from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.database.user import Users


class UserRepository:

    def __init__(self, session: Session):
        self.session = session

    def get_by_email(self, mail: str) -> Users | None:

        statement = select(Users).where(
            Users.mail == mail
        )

        return self.session.execute(
            statement
        ).scalar_one_or_none()

    def create_user(
        self,
        name: str,
        mail: str,
        password: str,
    ) -> Users:

        user = Users(
            name=name,
            mail=mail,
            password=password,
        )

        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)

        return user