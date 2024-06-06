from aiogram.types import User
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.text import Format
from aiogram_dialog.widgets.input import TextInput

from bot.states import FSMAddNote


async def username_getter(dialog_manager: DialogManager, event_from_user: User, **kwargs):
    return {'username': event_from_user.first_name}


start_dialog = Dialog(
    Window(
        Format("Давай добавим заметку {username}.\nНапиши текс заметки и нажми кнопку отправить."),
        TextInput(
            id="age_input",
        ),
        getter=username_getter,
        state=FSMAddNote.start,
    ),
    Window(
        Format("Data"),
        TextInput(
            id="age_input",
        ),
        state=FSMAddNote.text_note,
    ),
    Window(
        Format("End"),
        state=FSMAddNote.date,
    ),
)
