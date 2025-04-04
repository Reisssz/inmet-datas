FROM python:3.12-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir --upgrade pip && pip install -r requirements.txt

ENTRYPOINT ["python", "main.py"]
