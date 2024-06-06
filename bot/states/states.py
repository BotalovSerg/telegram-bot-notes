from aiogram.fsm.state import State, StatesGroup


class FSMAddNote(StatesGroup):
    text_note = State()
    date = State()
    