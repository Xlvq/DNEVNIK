from aiogram import Router
from aiogram.types import Message
from src.database import users

router = Router()

@router.message(commands=["add_grade"])
async def add_grade_command(message: Message):
    user_id = message.from_user.id
    if user_id not in users:
        await message.answer("Вы не авторизованы. Введите /auth для авторизации.")
        return

    try:
        _, subject, grade = message.text.split()
        grade = int(grade)
        if subject not in users[user_id]["grades"]:
            users[user_id]["grades"][subject] = []
        users[user_id]["grades"][subject].append(grade)
        await message.answer(f"Оценка {grade} по предмету {subject} успешно добавлена!")
    except ValueError:
        await message.answer("Неверный формат. Используйте: /add_grade <предмет> <оценка>")

@router.message(commands=["grades"])
async def view_grades_command(message: Message):
    user_id = message.from_user.id
    if user_id not in users:
        await message.answer("Вы не авторизованы. Введите /auth для авторизации.")
        return

    grades = users[user_id]["grades"]
    if not grades:
        await message.answer("У вас пока нет оценок.")
        return

    response = "Ваши оценки:\n"
    for subject, marks in grades.items():
        response += f"{subject}: {', '.join(map(str, marks))}\n"
    await message.answer(response)
