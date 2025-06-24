from src.database import User, SessionLocal


def set_admin(user_id: int):
    db = SessionLocal()
    try:
        # Найдем пользователя по user_id
        user = db.query(User).filter(User.user_id == user_id).first()
        if user:
            user.role = "admin"  # Устанавливаем роль admin
            db.commit()  # Сохраняем изменения
            print(f"Роль пользователя {user.name} изменена на admin.")
        else:
            print(f"Пользователь с ID {user_id} не найден.")
    except Exception as e:
        print(f"Ошибка при обновлении роли: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    # Пример вызова функции для вашего user_id
    set_admin(1284813556)  # Замените на ваш реальный user_id
