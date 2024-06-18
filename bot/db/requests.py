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


async def add_note(session: AsyncSession, data_note: dict, user_id: int) -> None:
    # await create_user(session, user_id)
    note = Note(
        note=data_note["note"],
        date=data_note["date"],
        telegram_id=user_id
    )
    session.add(note)
    await session.commit()


async def get_notes(session: AsyncSession, user_id: int):
    res = await session.scalars(select(Note).where(Note.telegram_id == user_id))
    return res.all()


async def get_note_by_uuid_id(session: AsyncSession, note_id: str) -> Note | None:
    note = await session.scalar(select(Note).where(Note.note_id == note_id))
    return note


async def delete_note(session: AsyncSession, note_id: str) -> None:
    existing_note = await get_note_by_uuid_id(session, note_id)
    if existing_note is None:
        return
    await session.delete(existing_note)
    await session.commit()


async def test_connection(session: AsyncSession):
    """
    Проверка соединения с СУБД
    :param session: объект AsyncSession
    """
    stmt = select(1)
    return await session.scalar(stmt)
