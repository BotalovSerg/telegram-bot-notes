from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.requests import create_user, get_user_by_id
from bot.lexicon.lexicon_ru import LEXICON

router = Router()


@router.message(CommandStart())
async def cmd_press_start(message: Message, session: AsyncSession) -> None:
    name_user = message.from_user.full_name
    user_id = message.from_user.id
    await create_user(session, user_id, name_user)

    await message.answer(text=LEXICON['command'][message.text])


@router.message(Command(commands="help"))
async def cmd_press_help(message: Message, session: AsyncSession) -> None:
    user_id = await get_user_by_id(session, message.from_user.id)
    await message.answer(text=LEXICON['command'][message.text])
    await message.answer(
        text=f"\nInfo User:"
             f"\nID: {user_id.telegram_id}"
             f"\nFull name: {message.from_user.full_name}")
