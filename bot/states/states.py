from aiogram.fsm.state import State, StatesGroup


class FSMAddNote(StatesGroup):
    start = State()
    text_note = State()
    date = State()
