from .auth import router as auth_router
from .grades import router as grades_router
from .main_router import main_router

__all__ = ["auth_router", "grades_router", "main_router"]
