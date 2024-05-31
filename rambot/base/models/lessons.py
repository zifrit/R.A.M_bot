from typing import TYPE_CHECKING

from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, ForeignKey, TEXT, Boolean
from sqlalchemy.dialects.postgresql import JSON
from base.models import Base

if TYPE_CHECKING:
    from base.models.user import ProfileStudent, ProfileTeacher


class Lesson(Base):
    __tablename__ = "lessons"
    name: Mapped[str] = mapped_column(String(255), unique=True)
    teacher_id: Mapped[int] = mapped_column(ForeignKey("profiles_teacher.id"))

    tasks: Mapped["Tasks"] = relationship(back_populates="lessons")
    teacher: Mapped["ProfileTeacher"] = relationship(back_populates="lessons")


class CompletedLesson(Base):
    __tablename__ = "completed_lessons"
    name: Mapped[str] = mapped_column(String(255), unique=True)
    teacher_id: Mapped[int] = mapped_column(ForeignKey("profiles_teacher.id"))
    student_id: Mapped[int] = mapped_column(ForeignKey("profiles_student.id"))

    student: Mapped["ProfileStudent"] = relationship(back_populates="completed_lessons")
    teacher: Mapped["ProfileTeacher"] = relationship(back_populates="completed_lessons")
    completed_tasks: Mapped["CompletedTasks"] = relationship(
        back_populates="completed_lessons"
    )


class Tasks(Base):
    __tablename__ = "tasks"
    task_type_id: Mapped[int] = mapped_column(ForeignKey("task_types.id"))
    lesson_id: Mapped[int] = mapped_column(ForeignKey("lessons.id"))
    question: Mapped[str] = mapped_column(TEXT())
    answer: Mapped[list | None] = mapped_column(JSON())

    task_types: Mapped["TasksTypes"] = relationship(back_populates="tasks")
    lessons: Mapped["Lesson"] = relationship(back_populates="tasks")


class CompletedTasks(Base):
    __tablename__ = "completed_tasks"
    task_type_id: Mapped[int] = mapped_column(ForeignKey("task_types.id"))
    completed_lesson_id: Mapped[int] = mapped_column(ForeignKey("completed_lessons.id"))
    student_id: Mapped[int] = mapped_column(ForeignKey("profiles_student.id"))
    question: Mapped[str] = mapped_column(TEXT())
    answer: Mapped[list | None] = mapped_column(JSON())
    system_verify: Mapped[bool] = mapped_column(default=False)
    teacher_verify: Mapped[bool] = mapped_column(default=False)

    task_types: Mapped["TasksTypes"] = relationship(back_populates="completed_tasks")
    completed_lessons: Mapped["CompletedLesson"] = relationship(
        back_populates="completed_tasks"
    )
    student: Mapped["ProfileStudent"] = relationship(back_populates="completed_tasks")


class TasksTypes(Base):
    __tablename__ = "task_types"
    name: Mapped[str] = mapped_column(String(255))

    tasks: Mapped["Tasks"] = relationship(back_populates="task_types")
    completed_tasks: Mapped["CompletedTasks"] = relationship(
        back_populates="task_types"
    )
