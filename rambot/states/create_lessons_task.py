from aiogram.fsm.state import StatesGroup, State


class CreateLesson(StatesGroup):
    name_lesson = State()
    description = State()


class UpdateLessonName(StatesGroup):
    id_lesson = State()
    new_name = State()


class CreateLessonTask(StatesGroup):
    id_lesson = State()
    img = State()
    question = State()
    answer = State()
    right_answer = State()
    task_type_id = State()
    next = State()
    previous = State()


class PaginationTask(StatesGroup):
    id_lesson = State()
