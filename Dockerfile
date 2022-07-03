FROM ghcr.io/opencirclepkgs/flask_base:latest

RUN mkdir /app
WORKDIR /app

COPY app.py .
COPY wsgi.py .
COPY backend ./backend
EXPOSE 5000

ENTRYPOINT ["python", "./wsgi.py"]
