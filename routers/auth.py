from aiogram import Router
from aiogram.types import Message
from src.database import users

router = Router()

@router.message(commands=["auth"])
async def auth_command(message: Message):
    user_id = message.from_user.id
    if user_id not in users:
        users[user_id] = {"name": message.from_user.first_name, "grades": {}}
        await message.answer("Вы успешно авторизованы!")
    else:
        await message.answer("Вы уже авторизованы!")
