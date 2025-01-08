from pathlib import Path

from dotenv import load_dotenv
import os


load_dotenv()


DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_PORT = os.environ.get('DB_PORT', '5432')
DB_NAME = os.environ.get('POSTGRES_DB')
DB_USER = os.environ.get('POSTGRES_USER')
DB_PASS = os.environ.get('POSTGRES_PASSWORD')
AUTH_SECRET = os.environ.get('AUTH_SECRET')

# Директория для сохранения загруженных фото
UPLOAD_PHOTO_DIR = Path('static/photos')
UPLOAD_PHOTO_DIR.mkdir(parents=True, exist_ok=True)

# Поддерживаемые форматы изображений
ALLOWED_EXTENSIONS = ("png", "jpg", "jpeg")
MAX_FILE_SIZE = 2 * 1024 * 1024  # Ограничение на 2 МБ
TARGET_SIZE = (1024, 1024)  # Целевой размер изображения
