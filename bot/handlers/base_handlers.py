from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.requests import create_user

router = Router()


@router.message(CommandStart())
async def cmd_press_start(message: Message, session: AsyncSession) -> None:
    name_user = message.from_user.full_name
    user_id = message.from_user.id
    await create_user(session, user_id, name_user)

    await message.answer(text="Hello")
