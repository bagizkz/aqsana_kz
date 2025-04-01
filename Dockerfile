# Используем минимальный образ Python
FROM python:3.13-slim

# Устанавливаем system-зависимости
RUN apt-get update && apt-get install -y curl build-essential

# Устанавливаем Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

# Директория проекта внутри контейнера
WORKDIR /app

# Копируем зависимости
COPY pyproject.toml poetry.lock* ./
RUN poetry install --no-root

COPY . .

EXPOSE 8000

CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]