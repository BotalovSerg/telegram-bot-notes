from aiogram import Router, F
from aiogram.types import Message

from bot.config_data.config import settings

router = Router()


@router.message(F.from_user.id.in_(settings.admins.ids_list), F.text == "secret")
async def admins_hello(message: Message):
    await message.reply("Hi, admin")