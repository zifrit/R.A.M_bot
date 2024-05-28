from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy import String


class Base(DeclarativeBase):
    __abstract__ = True
    id: Mapped[int] = mapped_column(primary_key=True)
