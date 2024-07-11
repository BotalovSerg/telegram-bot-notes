from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from bot.states.states import AddNoteSG
from bot.db.requests import get_notes, delete_note, get_note_by_uuid_id
from bot.lexicon.lexicon_ru import LEXICON
from bot.keyboards.notes_kb import create_notes_keyboard, create_edit_keyboard, save_note_keyboard
from bot.filters.filters import IsDelNoteCallbackData, IsIdNoteUUID
from bot.db.requests import add_note

router = Router()


@router.message(Command(commands="addnote"))
async def command_add_note(message: Message, state: FSMContext) -> None:
    await message.answer(text=LEXICON["command"][message.text])

    await state.set_state(AddNoteSG.text_note)


@router.message(AddNoteSG.text_note)
async def process_text_note_sent(message: Message, state: FSMContext) -> None:
    await state.update_data(text_note=message.text)

    await message.answer(
        text="Отлично!\n\nТеперь укажи время и дату или можешь просто написать "
             "'Сегодя', 'Завтра' или 'Всегда' :)"
    )
    await state.set_state(AddNoteSG.date_note)


@router.message(AddNoteSG.date_note)
async def process_date_sent(message: Message, state: FSMContext) -> None:
    await state.update_data(date_note=message.text)
    data_note = await state.get_data()
    await message.answer(
        text="Почти все готово, давай проверим перед сохранением"
             f"\nЗаметка: {data_note['text_note']}"
             f"\nВремя: {data_note['date_note']}",
        reply_markup=save_note_keyboard(),
    )
    await state.set_state(AddNoteSG.check_note)


@router.callback_query(F.data == "save_note", AddNoteSG.check_note)
async def process_check_note(callback: CallbackQuery, state: FSMContext, session: AsyncSession) -> None:
    data_note = await state.get_data()
    await state.clear()
    await callback.message.edit_text(text=LEXICON["command"]["end_state_add_note"])
    await callback.answer(text="✅")

    await add_note(session, data_note, callback.from_user.id)


@router.message(Command(commands="showallnotes"))
async def process_show_notes_sent(message: Message, session: AsyncSession) -> None:
    user_id = message.from_user.id
    all_notes = await get_notes(session, user_id)
    if all_notes:
        await message.answer(
            text=LEXICON["command"][message.text],
            reply_markup=create_notes_keyboard(all_notes)
        )
    else:
        await message.answer(
            text=LEXICON["command"]["no_notes"]
        )


@router.callback_query(F.data == "edit_notes")
async def process_edit_notes_press(callback: CallbackQuery, session: AsyncSession) -> None:
    user_id = callback.from_user.id
    all_notes = await get_notes(session, user_id)
    await callback.message.edit_text(
        text=LEXICON["command"][callback.data],
        reply_markup=create_edit_keyboard(all_notes)
    )
    await callback.answer(text="Edit")


@router.callback_query(IsDelNoteCallbackData())
async def process_del_notes_press(callback: CallbackQuery, session: AsyncSession) -> None:
    await delete_note(session, callback.data[:-3])
    user_id = callback.from_user.id
    all_notes = await get_notes(session, user_id)
    if all_notes:
        await callback.message.edit_text(
            text=LEXICON["command"]["edit_notes"],
            reply_markup=create_edit_keyboard(all_notes)
        )
    else:
        await callback.message.edit_text(
            text=LEXICON["command"]["no_notes"]
        )
    await callback.answer()


@router.callback_query(F.data == "cancel")
async def process_cancel_press(callback: CallbackQuery) -> None:
    await callback.message.edit_text(text=LEXICON["command"]["cancel_text"])
    await callback.answer(text="✅")


@router.callback_query(IsIdNoteUUID())
async def show_note(callback: CallbackQuery, session: AsyncSession) -> None:
    data_note = await get_note_by_uuid_id(session, callback.data)
    await callback.message.edit_text(
        text=f"Date: {data_note.date}\n"
             f"Note content: {data_note.note}",
    )
    await callback.answer()
