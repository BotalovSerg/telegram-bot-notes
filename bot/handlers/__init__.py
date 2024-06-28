from aiogram import Router

from .base_handlers import router as base_router
from .note_handlers import router as add_note_router
from .admin_hendlers import router as admin_router


def get_routes() -> list[Router]:
    return [
        base_router,
        add_note_router,
        admin_router,
    ]
