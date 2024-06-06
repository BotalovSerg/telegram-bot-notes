from aiogram.types import User
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.text import Format

from bot.states import FSMAddNote


async def username_getter(dialog_manager: DialogManager, event_from_user: User, **kwargs):
    return {'username': event_from_user.username}


start_dialog = Dialog(
    Window(
        Format('Привет, {username}!'),
        getter=username_getter,
        state=FSMAddNote.text_note
    ),
)
