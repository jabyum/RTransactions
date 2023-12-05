FROM python:3.9
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir telebot
CMD ["python", "mainbot.py"]