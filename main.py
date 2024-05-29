import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from bot.config_data.config import settings
from bot.handlers import get_routes


async def main() -> None:

    storage: MemoryStorage = MemoryStorage()
    bot: Bot = Bot(
        token=settings.bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp: Dispatcher = Dispatcher(storage=storage)
    dp.include_routers(*get_routes())

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
