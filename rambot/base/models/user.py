from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String

from base.models import Base


class User(Base):
    __tablename__ = "users"
    username: Mapped[str] = mapped_column(String(255), unique=True)
    first_name: Mapped[str | None] = mapped_column(String(255))


class ProfileTeacher(Base):
    __tablename__ = "profiles_teacher"
    first_name: Mapped[str] = mapped_column(String(255))
    last_name: Mapped[str] = mapped_column(String(255))
    middle_name: Mapped[str | None] = mapped_column(String(255))
