from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram_dialog import DialogManager, StartMode
from aiogram.fsm.context import FSMContext

from bot.states import FSMAddNote


router = Router()


@router.message(Command(commands='addnote'))
async def command_add_note(message: Message, dialog_manager: DialogManager) -> None:
    await dialog_manager.start(state=FSMAddNote.start, mode=StartMode.RESET_STACK)


@router.message(FSMAddNote.text_note)
async def process_text_note_sent(message: Message, state: FSMContext) -> None:
    await state.update_data(note=message.text)
    await message.answer(text='Отлично!\n\nТеперь укажи время и дату или можешь просто написать '
                              '"Сегодя", "Завтра" или "Всегда :)"')
    await state.set_state(FSMAddNote.date)


@router.message(FSMAddNote.date)
async def process_date_sent(message: Message, state: FSMContext) -> None:
    await state.update_data(date=message.text)
    data_note = await state.get_data()
    await message.answer(text="DONE")
    await state.clear()

    print(data_note)
    # await add_note(session, data_note, message.from_user.id)
