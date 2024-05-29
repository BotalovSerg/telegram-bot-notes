from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart


router = Router()


@router.message(CommandStart())
async def cmd_press_start(message: Message) -> None:
    await message.answer(text="Hello")
