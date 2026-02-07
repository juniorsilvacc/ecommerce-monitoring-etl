FROM python:3.12-slim

WORKDIR /app

# Instala dependências do sistema necessárias para o Pandas/PyArrow
RUN apt-get update && apt-get install -y libpq-dev gcc

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]