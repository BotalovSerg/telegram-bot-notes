from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram_dialog import DialogManager, StartMode
from sqlalchemy.ext.asyncio import AsyncSession

from bot.states import FSMAddNote
from bot.db.requests import get_notes, delete_note
from bot.lexicon.lexicon_ru import LEXICON
from bot.keyboards.notes_kb import create_notes_keyboard, create_edit_keyboard
from bot.filters.filters import IsDelNoteCallbackData

router = Router()


@router.message(Command(commands='addnote'))
async def command_add_note(message: Message, dialog_manager: DialogManager, session: AsyncSession) -> None:
    await dialog_manager.start(state=FSMAddNote.start, mode=StartMode.RESET_STACK, data={"session": session})


@router.message(Command(commands='showallnotes'))
async def process_show_notes_sent(message: Message, session: AsyncSession) -> None:
    user_id = message.from_user.id
    all_notes = await get_notes(session, user_id)
    if all_notes:
        await message.answer(
            text=LEXICON['command'][message.text],
            reply_markup=create_notes_keyboard(all_notes)
        )
    else:
        await message.answer(
            text=LEXICON['command']['no_notes']
        )


@router.callback_query(F.data == 'edit_notes')
async def process_edit_notes_press(callback: CallbackQuery, session: AsyncSession) -> None:
    user_id = callback.from_user.id
    all_notes = await get_notes(session, user_id)
    await callback.message.edit_text(
        text=LEXICON['command'][callback.data],
        reply_markup=create_edit_keyboard(all_notes)
    )
    await callback.answer(text='Edit')


@router.callback_query(IsDelNoteCallbackData())
async def process_del_notes_press(callback: CallbackQuery, session: AsyncSession) -> None:
    await delete_note(session, callback.data[:-3])
    user_id = callback.from_user.id
    all_notes = await get_notes(session, user_id)
    if all_notes:
        await callback.message.edit_text(
            text=LEXICON['command']['edit_notes'],
            reply_markup=create_edit_keyboard(all_notes)
        )
    else:
        await callback.message.edit_text(
            text=LEXICON['command']['no_notes']
        )
    await callback.answer()


@router.callback_query(F.data == 'cancel')
async def process_cancel_press(callback: CallbackQuery) -> None:
    await callback.message.edit_text(text=LEXICON['command']['cancel_text'])
    await callback.answer(text='✅')
