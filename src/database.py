from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

DATABASE_URL = "sqlite:///./test.db"  # Путь к вашей базе данных

# Создаем движок и сессию
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Определение модели пользователя
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, unique=True, index=True)
    name = Column(String, nullable=False)
    role = Column(String, default="student")

    # Связь с оценками
    grades = relationship("Grade", back_populates="user")


# Определение модели оценки
class Grade(Base):
    __tablename__ = "grades"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    subject = Column(String, index=True)
    grade = Column(Integer)

    user = relationship("User", back_populates="grades")

# Создание всех таблиц
Base.metadata.create_all(bind=engine)
