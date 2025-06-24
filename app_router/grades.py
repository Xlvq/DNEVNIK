
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

# Функция для обновления роли пользователя
def update_user_role(db: Session, user_id: int, new_role: str):
    user = db.query(User).filter(User.user_id == user_id).first()
    if user:
        user.role = new_role
        db.commit()
        db.refresh(user)
        return user
    return None

# Функция для добавления оценки
def add_grade(db: Session, user_id: int, subject: str, grade: int):
    new_grade = Grade(user_id=user_id, subject=subject, grade=grade)
    db.add(new_grade)
    db.commit()

# Функция для получения всех оценок
def get_grades(db: Session):
    return db.query(Grade).all()


def get_grades_by_user(db: Session, user_id: int):
    """Retrieve grades for a specific user."""
    return db.query(Grade).filter(Grade.user_id == user_id).all()

# Обработчик добавления оценки (только для учителей)
@router.message(F.text.startswith("/add_grade"))
async def add_grade_command(message: Message):
    """Добавление оценки студенту. Команда: /add_grade <user_id> <subject> <grade>"""
    teacher_id = message.from_user.id

    with SessionLocal() as db:
        user = get_user(db, teacher_id)
        if not user:
            await message.answer("Вы не авторизованы. Введите /auth для авторизации.")
            return

        if user.role != "teacher":
            await message.answer("У вас нет прав для добавления оценок.")
            return

        try:
            _, student_id_str, subject, grade_str = message.text.split()
            student_id = int(student_id_str)
            grade = int(grade_str)
        except ValueError:
            await message.answer(
                "Неверный формат. Используйте: /add_grade <id> <предмет> <оценка>"
            )
            return

        add_grade(db, student_id, subject, grade)
        await message.answer(
            f"Оценка {grade} по предмету {subject} студенту {student_id} успешно добавлена!"
        )


@router.message(F.text.startswith("/my_grades"))
async def my_grades_command(message: Message):
    """Вывод оценок текущего пользователя."""
    user_id = message.from_user.id

    with SessionLocal() as db:
        user = get_user(db, user_id)
        if not user:
            await message.answer("Вы не авторизованы. Введите /auth для авторизации.")
            return

        grades = get_grades_by_user(db, user_id)
        if not grades:
            await message.answer("У вас ещё нет оценок.")
        else:
            response = "Ваши оценки:\n"
            for grade in grades:
                response += f"{grade.subject}: {grade.grade}\n"
            await message.answer(response)

# Обработчик просмотра оценок (доступно администраторам и директорам)
@router.message(F.text.startswith("/grades"))
async def view_grades_command(message: Message):
    user_id = message.from_user.id

    with SessionLocal() as db:
        user = get_user(db, user_id)
        if not user:
            await message.answer("Вы не авторизованы. Введите /auth для авторизации.")
            return

        if user.role not in ["admin", "director"]:
            await message.answer("У вас нет прав для просмотра всех оценок.")
            return

        grades = get_grades(db)
        if not grades:
            await message.answer("В базе данных нет оценок.")
            return

        response = "Все оценки:\n"
        for grade in grades:
            response += f"{grade.subject}: {grade.grade}\n"

        await message.answer(response)

