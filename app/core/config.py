import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent.parent
TEMPLATE_DIR = BASE_DIR / "app" / "templates"
STATIC_DIR = BASE_DIR / "app" / "static"

# Параметры PostgreSQL
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')

# Параметры Redis
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')
REDIS_USER = os.getenv('REDIS_USER')
REDIS_USER_PASSWORD = os.getenv('REDIS_USER_PASSWORD')
REDIS_PORT = os.getenv('REDIS_PORT')

# Авторизация
PRIVATE_KEY_PATH: Path = BASE_DIR / "certs" / "jwt-private.pem"
PUBLIC_KEY_PATH: Path = BASE_DIR / "certs" / "jwt-public.pem"
ALGORITHM: str = "RS256"

TOKEN_TYPE_FIELD = "type"
ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"

ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
REFRESH_TOKEN_EXPIRE_DAYS: int = 30

# Middleware
PUBLIC_PATHS = ["/login", "/docs"]
PUBLIC_PATH_PREFIXES = ["/static", "/api"]
