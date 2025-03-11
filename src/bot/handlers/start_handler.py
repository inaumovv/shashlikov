from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from src import container

router: Router = Router()


@router.message(CommandStart())
async def start(message: Message, con=container):
    await message.answer(
        'Демонстрационный бот кафе "Шашлыкофф".'
        '\nДля продолжения напишите любое сообщение, например, "здравствуйте".'
        '\n\n© Badge Company',
        reply_markup=con.keyboards.start_inline_keyboard()
    )
