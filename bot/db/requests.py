from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.models import User, Note


async def get_user_by_id(session: AsyncSession, user_id: int) -> User | None:
    stmt = select(User).where(User.telegram_id == user_id)
    return await session.scalar(stmt)


async def create_user(session: AsyncSession, user_id: int, full_name: str) -> None:
    existing_user = await get_user_by_id(session, user_id)
    if existing_user is not None:
        return
    user = User(
        telegram_id=user_id,
        fullname=full_name,
    )
    session.add(user)
    await session.commit()


async def test_connection(session: AsyncSession):
    """
    Проверка соединения с СУБД
    :param session: объект AsyncSession
    """
    stmt = select(1)
    return await session.scalar(stmt)
