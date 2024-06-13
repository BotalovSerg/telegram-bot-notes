import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram_dialog import setup_dialogs
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from bot.config_data.config import settings
from bot.handlers import get_routes
from bot.dialogs import get_dialog
from bot.db.requests import test_connection


logger = logging.getLogger(__name__)


async def main() -> None:

    engine = create_async_engine(url=str(settings.db.url), echo=True)
    session_maker = async_sessionmaker(engine, expire_on_commit=False)

    async with session_maker() as session:
        await test_connection(session)
    logger.info("Connect db")

    storage: MemoryStorage = MemoryStorage()
    bot: Bot = Bot(
        token=settings.bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp: Dispatcher = Dispatcher(storage=storage)
    dp.include_routers(
        *get_routes(),
        *get_dialog()
    )
    setup_dialogs(dp)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
