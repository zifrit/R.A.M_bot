from aiogram.fsm.state import StatesGroup, State


class CreateLesson(StatesGroup):
    name_lesson = State()


class UpdateLessonName(StatesGroup):
    id_lesson = State()
    new_name = State()
