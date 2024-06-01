from aiogram.fsm.state import StatesGroup, State


class CreateProfileStudent(StatesGroup):
    FIO = State()
    first_name = State()
    last_name = State()
    middle_name = State()


class CreateProfileTeacher(StatesGroup):
    FIO = State()
    first_name = State()
    last_name = State()
    middle_name = State()
    bio = State()
    image = State()
