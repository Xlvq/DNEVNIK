from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from src.database import SessionLocal, User

router = Router()

# Функция для работы с базой данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Определяем состояния FSM
class SetRoleStates(StatesGroup):
    waiting_for_user_id = State()
    waiting_for_role = State()

# Обработчик команды /start
@router.message(Command(commands=["start"]))
async def start(message: Message):
    db = next(get_db())
    user = db.query(User).filter(User.user_id == message.from_user.id).first()

    if user:
        await message.reply(f"Привет, {user.name}!")
    else:
        # Если пользователь не найден, добавляем его в базу данных
        new_user = User(user_id=message.from_user.id, name=message.from_user.full_name, role="student")
        db.add(new_user)
        db.commit()
        await message.reply("Привет! Вы были зарегистрированы как новый пользователь с ролью 'student'.")

# Обработчик команды /auth
@router.message(Command(commands=["auth"]))
async def auth_command(message: Message):
    """Обработчик команды /auth."""
    db = next(get_db())
    user = db.query(User).filter(User.user_id == message.from_user.id).first()

    if user:
        await message.reply(f"Вы авторизованы как: {user.name}. Ваша роль: {user.role}.")
    else:
        # Если пользователь не найден, добавляем его в базу данных
        new_user = User(user_id=message.from_user.id, name=message.from_user.full_name, role="student")
        db.add(new_user)
        db.commit()
        await message.reply("Вы были зарегистрированы как новый пользователь с ролью 'student'.")

# Обработчик команды /set_role
@router.message(Command(commands=["set_role"]))
async def set_role_start(message: Message, state: FSMContext):
    """Обработчик начала команды /set_role."""
    db = next(get_db())
    # Проверяем, является ли пользователь администратором
    user = db.query(User).filter(User.user_id == message.from_user.id).first()
    if user is None or user.role != "admin":
        await message.reply("У вас нет прав на выполнение этой команды.")
        return

    # Начинаем FSM и запрашиваем ID пользователя
    await message.reply("Введите ID пользователя, которому вы хотите назначить роль:")
    await state.set_state(SetRoleStates.waiting_for_user_id)

# Обработчик ввода ID пользователя
@router.message(SetRoleStates.waiting_for_user_id)
async def process_user_id(message: Message, state: FSMContext):
    """Обработчик ввода ID пользователя."""
    try:
        user_id = int(message.text)  # Проверяем, что это число
    except ValueError:
        await message.reply("Пожалуйста, введите корректный ID (число).")
        return

    # Сохраняем ID пользователя и переходим к следующему состоянию
    await state.update_data(user_id=user_id)
    await message.reply("Введите новую роль для пользователя (например: `student`, `teacher`, `admin`):")
    await state.set_state(SetRoleStates.waiting_for_role)

# Обработчик ввода новой роли
@router.message(SetRoleStates.waiting_for_role)
async def process_role(message: Message, state: FSMContext):
    """Обработчик ввода новой роли."""
    new_role = message.text.strip()

    # Проверяем, что роль допустима
    valid_roles = ["student", "teacher", "admin"]
    if new_role not in valid_roles:
        await message.reply(f"Недопустимая роль '{new_role}'. Допустимые роли: {', '.join(valid_roles)}")
        return

    # Получаем сохранённый user_id из состояния
    data = await state.get_data()
    user_id = data.get("user_id")

    # Подключаемся к базе данных и обновляем роль
    db = next(get_db())
    target_user = db.query(User).filter(User.user_id == user_id).first()
    if not target_user:
        await message.reply(f"Пользователь с ID {user_id} не найден.")
    else:
        target_user.role = new_role
        db.commit()
        await message.reply(f"Роль пользователя с ID {user_id} успешно обновлена на '{new_role}'.")

    # Завершаем FSM
    await state.clear()
