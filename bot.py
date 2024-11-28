from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import BOT_TOKEN
from app_router.auth import router as auth_router
from app_router.grades import router as grades_router
from app_router.main_router import main_router as main_router  # Теперь это должно работать

bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Регистрация роутеров
dp.include_router(auth_router)
dp.include_router(grades_router)
dp.include_router(main_router)

# Запуск бота
async def main():
    print("Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
