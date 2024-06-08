from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram_dialog import DialogManager, StartMode

from bot.states import FSMAddNote


router = Router()


@router.message(Command(commands='addnote'))
async def command_add_note(message: Message, dialog_manager: DialogManager) -> None:
    await dialog_manager.start(state=FSMAddNote.start, mode=StartMode.RESET_STACK)
