import enum
from typing import TYPE_CHECKING

from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, ForeignKey, TEXT, Boolean, Float, Enum
from sqlalchemy.dialects.postgresql import JSON
from base.models import Base

if TYPE_CHECKING:
    from base.models.user import ProfileStudent, ProfileTeacher


class Lesson(Base):
    __tablename__ = "lessons"
    name: Mapped[str] = mapped_column(String(255), unique=True)
    description: Mapped[str | None] = mapped_column(String(255))
    teacher_id: Mapped[int] = mapped_column(ForeignKey("profiles_teacher.id"))

    tasks: Mapped[list["Tasks"]] = relationship(back_populates="lessons")
    teacher: Mapped["ProfileTeacher"] = relationship(back_populates="lessons")

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id})"


class InProgressLesson(Base):
    __tablename__ = "in_progress_lessons"
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(String(255))
    point: Mapped[int | None]  # оценка для урок

    teacher_id: Mapped[int] = mapped_column(ForeignKey("profiles_teacher.id"))
    student_id: Mapped[int] = mapped_column(ForeignKey("profiles_student.id"))
    completed: Mapped[bool] = mapped_column(default=False)

    student: Mapped["ProfileStudent"] = relationship(
        back_populates="in_progress_lessons"
    )
    teacher: Mapped["ProfileTeacher"] = relationship(
        back_populates="in_progress_lessons"
    )
    in_progress_tasks: Mapped[list["InProgressTasks"]] = relationship(
        back_populates="in_progress_lessons",
        cascade="all, delete",
        passive_deletes=True,
    )


class Tasks(Base):
    __tablename__ = "tasks"
    task_type_id: Mapped[int] = mapped_column(ForeignKey("task_types.id"))
    lesson_id: Mapped[int] = mapped_column(ForeignKey("lessons.id"))
    next_task_id: Mapped[int | None] = mapped_column(
        ForeignKey("tasks.id", ondelete="set null")
    )
    previous_task_id: Mapped[int | None] = mapped_column(
        ForeignKey("tasks.id", ondelete="set null")
    )
    img: Mapped[str | None]
    question: Mapped[str] = mapped_column(TEXT())
    answer: Mapped[list] = mapped_column(JSON())
    right_answer: Mapped[str]

    task_types: Mapped["TasksTypes"] = relationship(back_populates="tasks")
    lessons: Mapped["Lesson"] = relationship(back_populates="tasks")

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id})"


class ProgressTask(enum.Enum):
    incomplete = "incomplete"
    now = "now"
    complete = "complete"


class InProgressTasks(Base):
    __tablename__ = "in_progress_tasks"
    task_type_id: Mapped[int] = mapped_column(ForeignKey("task_types.id"))
    in_progress_lessons_id: Mapped[int] = mapped_column(
        ForeignKey("in_progress_lessons.id")
    )
    next_task_id: Mapped[int | None]
    previous_task_id: Mapped[int | None]

    img: Mapped[str | None]
    question: Mapped[str] = mapped_column(TEXT())
    answer: Mapped[list] = mapped_column(JSON())
    right_answer: Mapped[str]
    progress: Mapped[str] = mapped_column(
        Enum(ProgressTask, name="progress"), default=ProgressTask.incomplete
    )
    student_answer: Mapped[str | None]
    system_verify: Mapped[bool] = mapped_column(default=False)
    teacher_verify: Mapped[bool] = mapped_column(default=False)

    task_types: Mapped["TasksTypes"] = relationship(back_populates="completed_tasks")
    in_progress_lessons: Mapped["InProgressLesson"] = relationship(
        back_populates="in_progress_tasks"
    )


class TasksTypes(Base):
    __tablename__ = "task_types"
    name: Mapped[str] = mapped_column(String(255))

    tasks: Mapped["Tasks"] = relationship(back_populates="task_types")
    completed_tasks: Mapped["InProgressTasks"] = relationship(
        back_populates="task_types"
    )
