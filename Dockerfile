FROM python:3.12-slim
WORKDIR /app
COPY . .
CMD ["sh", "-c", "python3 tracker.py & python3 bot.py & python3 server.py"]
