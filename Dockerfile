FROM ghcr.io/opencirclepkgs/flask_base:latest

RUN mkdir /app
WORKDIR /app

COPY backend ./backend
EXPOSE 5000

ENTRYPOINT ["python", "./backend/wsgi.py"]
