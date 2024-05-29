from aiogram import Router

from .basehandlers import router as base_router


def get_routes() -> list[Router]:
    return [
        base_router,
    ]
