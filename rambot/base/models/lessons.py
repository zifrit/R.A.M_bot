from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, ForeignKey, TEXT
from sqlalchemy.dialects.postgresql import JSON
from base.models import Base


class Lesson(Base):
    __tablename__ = "lessons"
    name: Mapped[str] = mapped_column(String(255), unique=True)
    tasks: Mapped["Tasks"] = relationship(back_populates="lessons")


class Tasks(Base):
    __tablename__ = "tasks"
    task_type_id: Mapped[int] = mapped_column(ForeignKey("task_types.id"))
    lesson_id: Mapped[int] = mapped_column(ForeignKey("lessons.id"))
    text: Mapped[str] = mapped_column(TEXT())
    answer: Mapped[list] = mapped_column(JSON())
    task_types: Mapped["TasksTypes"] = relationship(back_populates="tasks")
    lessons: Mapped["TasksTypes"] = relationship(back_populates="tasks")


class TasksTypes(Base):
    __tablename__ = "task_types"
    name: Mapped[str] = mapped_column(String(255))
    tasks: Mapped["Tasks"] = relationship(back_populates="task_types")
