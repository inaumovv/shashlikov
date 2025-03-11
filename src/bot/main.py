import asyncio
import logging
import os

from aiogram import Dispatcher

from src.bot.bot import bot
from src.bot.handlers.manager_handlers import router as manager_router
from src.bot.handlers.start_handler import router as start_router

dispatcher: Dispatcher = Dispatcher()
logging.basicConfig(level=logging.INFO)

logger: logging = logging.getLogger(__name__)

# os.environ["PATH"] = os.environ["PATH"] + r"D:\Other_files\ffmpeg\ffmpeg-master-latest-win64-gpl-shared\bin"


async def _register_routers() -> None:
    dispatcher.include_routers(start_router, manager_router)


async def _register_middleware() -> None:
    pass


@dispatcher.startup()
async def on_startup() -> None:
    # Register all routers
    await _register_routers()
    await _register_middleware()


async def run_polling() -> None:
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(run_polling())
