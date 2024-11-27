from aiogram import Router, F
from aiogram.types import Message
from sqlalchemy.orm import Session
from src.database import SessionLocal, Grade, User

router = Router()

# Функция для получения сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Добавление оценки (только для учителей)
@router.message(F.text.startswith("/add_grade"))
async def add_grade_command(message: Message):
    user_id = message.from_user.id
    db = next(get_db())

    # Проверяем роль пользователя
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        await message.answer("Вы не авторизованы. Введите /auth для авторизации.")
        return

    if user.role != "teacher":
        await message.answer("У вас нет прав для добавления оценок.")
        return

    try:
        _, subject, grade = message.text.split()
        grade = int(grade)

        # Добавляем оценку в базу данных
        new_grade = Grade(user_id=user_id, subject=subject, grade=grade)
        db.add(new_grade)
        db.commit()

        await message.answer(f"Оценка {grade} по предмету {subject} успешно добавлена!")
    except ValueError:
        await message.answer("Неверный формат. Используйте: /add_grade <предмет> <оценка>")

# Просмотр оценок (доступно администраторам и директорам)
@router.message(F.text.startswith("/grades"))
async def view_grades_command(message: Message):
    user_id = message.from_user.id
    db = next(get_db())

    # Проверяем роль пользователя
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        await message.answer("Вы не авторизованы. Введите /auth для авторизации.")
        return

    if user.role not in ["admin", "director"]:
        await message.answer("У вас нет прав для просмотра всех оценок.")
        return

    grades = db.query(Grade).all()
    if not grades:
        await message.answer("В базе данных нет оценок.")
        return

    # Формируем сообщение с оценками
    response = "Все оценки:\n"
    for grade in grades:
        response += f"{grade.subject}: {grade.grade}\n"

    await message.answer(response)
