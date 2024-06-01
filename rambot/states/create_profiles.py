from aiogram.fsm.state import StatesGroup, State


class CreateProfile(StatesGroup):
    FIO = State()
    first_name = State()
    last_name = State()
    middle_name = State()


class CreateProfileStudent(CreateProfile): ...


class CreateProfileTeacher(CreateProfile):
    bio = State()
    image = State()
