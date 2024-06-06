from aiogram import Router

from .basehandlers import router as base_router
from .add_note import router as add_note_router


def get_routes() -> list[Router]:
    return [
        base_router,
        add_note_router,
    ]
