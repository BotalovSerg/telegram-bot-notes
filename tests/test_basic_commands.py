from datetime import datetime

import pytest
from aiogram import Dispatcher
from aiogram.dispatcher.event.bases import UNHANDLED
from aiogram.enums import ChatType
from aiogram.methods import SendMessage
from aiogram.methods.base import TelegramType
from aiogram.types import Update, Chat, User, Message
from tests.mocked_aiogram import MockedBot
from bot.lexicon.lexicon_ru import LEXICON


def get_message(command: str) -> Message:
    message = Message(
        message_id=1,
        chat=Chat(id=1234567, type=ChatType.PRIVATE),
        from_user=User(id=1234567, is_bot=False, first_name="User"),
        text=command,
        date=datetime.now()
    )
    return message


@pytest.mark.asyncio
async def test_cmd_start(dp: Dispatcher, bot: MockedBot) -> None:
    bot.add_result_for(
        method=SendMessage,
        ok=True,
    )
    message = get_message(command='/start')
    result = await dp.feed_update(
        bot,
        Update(message=message, update_id=1)
    )
    assert result is not UNHANDLED
    outgoing_message: TelegramType = bot.get_request()
    assert isinstance(outgoing_message, SendMessage)
    assert outgoing_message.text == LEXICON['command']['/start']