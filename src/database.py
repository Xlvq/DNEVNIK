import sqlite3
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Настроим базу данных с использованием SQLite
DATABASE_URL = "sqlite:///./database.db"

# Настройка базы данных
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Таблица пользователей
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, unique=True, index=True)
    name = Column(String)
    role = Column(String, default="student")  # Новое поле для роли

# Таблица оценок
class Grade(Base):
    __tablename__ = "grades"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    subject = Column(String)
    grade = Column(Integer)

# Создание всех таблиц
def init_db():
    Base.metadata.create_all(bind=engine)
