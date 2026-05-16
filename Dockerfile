FROM python:3.9-slim

WORKDIR /app

COPY app/requirements.txt .
RUN pip install -r requirements.txt

COPY app/ .

# Running as root — Trivy should flag this
EXPOSE 5000

CMD ["python", "app.py"]