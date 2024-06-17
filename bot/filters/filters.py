import uuid
from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery


class IsDelNoteCallbackData(BaseFilter):
    @staticmethod
    def _is_valid_uuid(uuid_to_test: str, ver: int = 4) -> bool:
        try:
            uuid_obj = uuid.UUID(uuid_to_test, version=ver)
        except ValueError:
            return False
        return str(uuid_obj) == uuid_to_test

    async def __call__(self, callback: CallbackQuery) -> bool:
        data_uuid = callback.data[:-3]
        return callback.data.endswith('del') and self._is_valid_uuid(data_uuid)
