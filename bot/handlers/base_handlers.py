from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.requests import create_user, get_user_by_id

router = Router()


@router.message(CommandStart())
async def cmd_press_start(message: Message, session: AsyncSession) -> None:
    name_user = message.from_user.full_name
    user_id = message.from_user.id
    await create_user(session, user_id, name_user)

    await message.answer(text="Hello")


@router.message(Command(commands="whoami"))
async def cmd_press_who_am_i(message: Message, session: AsyncSession) -> None:
    user_id = await get_user_by_id(session, message.from_user.id)
    await message.answer(text=f"User: {message.from_user.full_name}, ID: {user_id.telegram_id}")
