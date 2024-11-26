from aiogram import Router
from aiogram.types import Message

router = Router()

@router.message(commands=["start"])
async def start_command(message: Message):
    await message.answer("Добро пожаловать в Электронный дневник!\nВведите /auth для авторизации.")
