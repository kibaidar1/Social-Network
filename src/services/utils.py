import re

from PIL import Image
from slugify import slugify

from src.config import ALLOWED_EXTENSIONS, MAX_FILE_SIZE, TARGET_SIZE, UPLOAD_PHOTO_DIR
from src.utils.unitofwork import UnitOfWork


def validate_and_save_photo(image_file: Image, filename: str):
    # Проверка расширения файла
    extension = image_file.filename.split(".")[-1].lower()
    if extension not in ALLOWED_EXTENSIONS:
        raise ValueError("Invalid file format")

        # Проверка размера файла
    image_file.file.seek(0, 2)  # Переход в конец файла для получения размера
    file_size = image_file.file.tell()
    image_file.file.seek(0)  # Возврат в начало файла для последующих операций
    if file_size > MAX_FILE_SIZE:
        raise ValueError("The file is too big")

    # Проверка, что файл действительно является изображением
    try:
        image = Image.open(image_file.file)
        image.verify()  # Проверка целостности изображения
        image = Image.open(image_file.file)
    except (IOError, SyntaxError):
        raise ValueError("The file is not a valid image")

    # Пропорциональное изменение размера с обрезкой
    image.thumbnail(TARGET_SIZE)
    if image.size != TARGET_SIZE:
        image = image.resize(TARGET_SIZE, Image.Resampling.LANCZOS)

    # Сохранение изображения в целевом формате
    image_path = f"{filename}.png"
    image.save(UPLOAD_PHOTO_DIR / image_path)

    return image_path


async def generate_unique_slug(uow: UnitOfWork, title: str) -> str:
    # Генерация начального slug на основе заголовка
    base_slug = slugify(title)

    # Проверяем, существует ли уже такой slug без числового суффикса
    async with uow:
        existing_post = await uow.posts.find_all(slug=base_slug)

        # Если точный slug существует, увеличиваем суффикс
        if existing_post:
            # Собираем все числовые суффиксы из базы данных для данного base_slug
            posts = await uow.posts.find_post_with_slug_like(f"{base_slug}-%")
            # Собираем все числовые суффиксы
            suffixes = set()
            for post in posts:
                match = re.match(r"^" + re.escape(base_slug) + r"-(\d+)$", post.slug)
                if match:
                    suffix = int(match.group(1))  # Извлекаем числовой суффикс
                    suffixes.add(suffix)

            # Находим первый пропущенный суффикс
            next_suffix = 1
            while next_suffix in suffixes:
                next_suffix += 1

            # Создаем новый slug с найденным суффиксом
            unique_slug = f"{base_slug}-{next_suffix}"
        else:
            # Если точный slug без суффикса не существует, то он уникален
            unique_slug = base_slug

    return unique_slug

