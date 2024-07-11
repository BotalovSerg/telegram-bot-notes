from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot.lexicon.lexicon_ru import LEXICON
from bot.db.models import Note


def create_notes_keyboard(notes: list[Note]) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    text_note: str
    for number, note in enumerate(notes, start=1):
        text_note = note.note if len(note.note) < 20 else note.note[:20] + '...'
        kb_builder.row(InlineKeyboardButton(
            text=f'{number}. Дата: {note.date} - {text_note}',
            callback_data=str(note.note_id)
        ))
    kb_builder.row(
        InlineKeyboardButton(
            text=LEXICON['command']['edit_notes_button'],
            callback_data='edit_notes'
        ),
        InlineKeyboardButton(
            text=LEXICON['command']['cancel'],
            callback_data='cancel'
        ),
        width=2
    )
    return kb_builder.as_markup()


def create_edit_keyboard(notes: list[Note]) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    for number, note in enumerate(notes, start=1):
        kb_builder.row(InlineKeyboardButton(
            text=f'❌ {number}. Дата: {note.date} - {note.note[:30]}',
            callback_data=f'{note.note_id}del'
        ))
    kb_builder.row(
        InlineKeyboardButton(
            text=LEXICON['command']['cancel'],
            callback_data='cancel'
        )
    )
    return kb_builder.as_markup()


def save_note_keyboard() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = [
        InlineKeyboardButton(text="Save", callback_data="save_note"),
        InlineKeyboardButton(text="Cansel", callback_data="cancel_save_note"),
    ]
    kb_builder.row(
        *buttons,
        width=2
    )
    return kb_builder.as_markup()
