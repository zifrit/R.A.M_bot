from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, ForeignKey, Table, Column, Integer, UniqueConstraint

from base.models import Base


class User(Base):
    __tablename__ = "users"
    username: Mapped[str] = mapped_column(String(255))
    tg_id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    is_student: Mapped[bool] = mapped_column(default=False)
    profile_student: Mapped["ProfileStudent"] = relationship(back_populates="user")
    is_teacher: Mapped[bool] = mapped_column(default=False)
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


association_student_teacher_table = Table(
    "association_student_teacher",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("profiles_student_id", ForeignKey("profiles_student.id"), nullable=False),
    Column("profiles_teacher_id", ForeignKey("profiles_teacher.id"), nullable=False),
    UniqueConstraint(
        "profiles_student_id", "profiles_teacher_id", name="idx_unique_student_teacher"
    ),
)
