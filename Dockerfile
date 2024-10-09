# Используем официальный образ Python в качестве базового
FROM python:3.12

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файл requirements.txt в контейнер
COPY requirements.txt /app/requirements.txt

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r /app/requirements.txt

# Копируем все файлы приложения в контейнер
COPY . /app

# Открываем порт 8000 для доступа к приложению
EXPOSE 8000

# Команда для запуска FastAPI с использованием Uvicorn
CMD ["uvicorn", "irisApp:app", "--host", "0.0.0.0", "--port", "8000"]