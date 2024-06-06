from aiogram_dialog import Dialog

from .dialog_add_note import start_dialog


def get_dialog() -> list[Dialog]:
    return [
        start_dialog,
    ]
