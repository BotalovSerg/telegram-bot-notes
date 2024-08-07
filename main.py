import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from bot.middlewares import DbSessionMiddleware
from bot.config_data.config import settings
from bot.handlers import get_routers
from bot.db.requests import test_connection
from bot.keyboards.set_menu import set_main_menu


logger = logging.getLogger(__name__)


async def main() -> None:

    engine = create_async_engine(url=str(settings.db.url), echo=False)
    session_maker = async_sessionmaker(engine, expire_on_commit=False)

    async with session_maker() as session:
        await test_connection(session)
    logger.info("Connect db")

    storage = RedisStorage.from_url(str(settings.redis.dsn))
    bot: Bot = Bot(
        token=settings.bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp: Dispatcher = Dispatcher(storage=storage)
    dp.update.middleware(DbSessionMiddleware(session_pool=session_maker))
    dp.include_routers(
        *get_routers(),
    )

    await set_main_menu(bot)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
