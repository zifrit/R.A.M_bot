from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, ForeignKey

from base.models import Base


class User(Base):
    __tablename__ = "users"
    username: Mapped[str] = mapped_column(String(255))
    tg_id: Mapped[int] = mapped_column(String(255), unique=True)
    is_student: Mapped[bool]
    profile_student: Mapped["ProfileTeacher"] = relationship(back_populates="user")
    is_teacher: Mapped[bool]
    profile_teacher: Mapped["ProfileTeacher"] = relationship(back_populates="user")


class ProfileTeacher(Base):
    __tablename__ = "profiles_teacher"
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        unique=True,
    )
    first_name: Mapped[str] = mapped_column(String(255))
    last_name: Mapped[str] = mapped_column(String(255))
    middle_name: Mapped[str | None] = mapped_column(String(255))
    user: Mapped["User"] = relationship(back_populates="profile_teacher")


class ProfileStudent(Base):
    __tablename__ = "profiles_student"
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        unique=True,
    )
    first_name: Mapped[str] = mapped_column(String(255))
    last_name: Mapped[str] = mapped_column(String(255))
    middle_name: Mapped[str | None] = mapped_column(String(255))
    user: Mapped["User"] = relationship(back_populates="profile_student")
