FROM python:3.11-slim-buster
ENV PYTHONUNBUFFERED True
WORKDIR /app
COPY *.txt .
RUN pip install --no-cache-dir --upgrade pip -r requirements.txt
COPY . ./
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]