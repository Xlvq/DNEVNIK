from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from sqlalchemy.orm import Session
from src.database import SessionLocal, User

main_router = Router()

# Функция для получения сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Функция для получения пользователя по user_id
def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.user_id == user_id).first()

# Функция для создания нового пользователя
def create_user(db: Session, user_id: int, name: str, role: str = "student"):
    db_user = User(user_id=user_id, name=name, role=role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@main_router.message(Command(commands=["start"]))
async def start(message: Message):
    # Используем обычный синхронный цикл с get_db
    db = next(get_db())  # Получаем сессию из генератора
    user = get_user(db, message.from_user.id)
    if user:
        await message.reply(f"Привет, {user.name}! Вы авторизованы как {user.role}.")
    else:
        # Если пользователь не найден, добавляем его в базу данных
        new_user = create_user(db, message.from_user.id, message.from_user.full_name, "student")
        await message.reply(f"Привет, {new_user.name}! Вы зарегистрированы как новый пользователь с ролью 'student'.")
