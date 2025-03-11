from aiogram.enums import ContentType, ParseMode

from src import container

from aiogram import Router, F
from aiogram.types import Message

from src.bot.bot import bot
from src.prompts import prompt_v1

router: Router = Router()


@router.message(F.text)
async def text_help(message: Message, con=container):
    answer: str = await con.openai_worker.get_product_info(
        query=message.text,
        user=message.from_user.id,
        prompt=prompt_v1
    )
    await message.answer(answer, parse_mode=ParseMode.MARKDOWN)


@router.message(F.content_type.in_({'voice'}))
async def voice_help(message: Message, con=container):
    file_id = message.voice.file_id
    file_info = await bot.get_file(file_id)
    file_path = file_info.file_path
    file_url = f"https://api.telegram.org/file/bot{bot.token}/{file_path}"
    query = con.recognizer.transcrible(file_url)

    answer: str = await con.openai_worker.get_product_info(
        query=query,
        user=message.from_user.id,
        prompt=prompt_v1
    )

    await message.answer(answer, parse_mode=ParseMode.MARKDOWN)
