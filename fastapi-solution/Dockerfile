FROM python:3.10.2-alpine
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN  \
    apk update && \
    apk upgrade && \
    pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY src/. .
CMD ["gunicorn", "main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8001"]