import sqlite3

# Подключаемся к базе данных
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Задайте ваш user_id (например, 1284813556)
user_id = 1284813556

# Обновляем роль пользователя на 'admin'
cursor.execute("UPDATE users SET role = 'admin' WHERE user_id = ?", (user_id,))

# Сохраняем изменения
conn.commit()

# Проверим, что роль обновлена
cursor.execute("SELECT user_id, name, role FROM users WHERE user_id = ?", (user_id,))
user = cursor.fetchone()
print(f"User ID: {user[0]}, Name: {user[1]}, Role: {user[2]}")

# Закрываем соединение
conn.close()
