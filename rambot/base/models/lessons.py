from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String
from base.models import Base


class Lesson(Base):
    __tablename__ = "lessons"
    name: Mapped[str] = mapped_column(String(255), unique=True)
