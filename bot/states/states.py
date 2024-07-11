from aiogram.fsm.state import State, StatesGroup


class AddNoteSG(StatesGroup):
    text_note = State()
    date_note = State()
    check_note = State()
