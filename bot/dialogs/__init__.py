from aiogram_dialog import Dialog

from .dialog_add_note import note_dialog


def get_dialog() -> list[Dialog]:
    return [
        note_dialog,
    ]
