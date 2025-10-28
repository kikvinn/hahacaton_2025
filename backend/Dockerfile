# Используем официальный образ Python 3.13 slim
FROM python:3.13-slim-bookworm

# Устанавливаем системные зависимости и uv


# Установка uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Копируем pyproject.toml и lock-файл
COPY pyproject.toml uv.lock* ./

# Устанавливаем зависимости в виртуальное окружение
RUN uv sync --locked --no-dev

# Копируем исходный код
COPY . .

# Открываем стандартный порт (фиксированное значение)
EXPOSE 8000

# Запуск через shell, чтобы подставились переменные окружения
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]