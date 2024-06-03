from aiogram.fsm.state import StatesGroup, State


class JoinToTeacher(StatesGroup):
    join_token = State()
