from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from sqlalchemy.orm import Session
from src.database import SessionLocal, User

main_router = Router()

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@main_router.message(Command(commands=["start"]))
async def start(message: Message):
    async for db in get_db():
        user = db.query(User).filter(User.user_id == message.from_user.id).first()
        if user:
            await message.reply(f"Привет, {user.name}! Вы авторизованы как {user.role}.")
        else:
            new_user = User(user_id=message.from_user.id, name=message.from_user.full_name, role="student")
            db.add(new_user)
            db.commit()
            await message.reply("Привет! Вы зарегистрированы как новый пользователь с ролью 'student'.")
