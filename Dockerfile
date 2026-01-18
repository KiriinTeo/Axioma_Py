# ok vamo lá, esse vai comentato certinho pra eu não me perder

FROM python:3.11-slim

# Evita arquivos .pyc e buffering estranho
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Diretório de trabalho dentro do container
WORKDIR /app

# Dependências do sistema (pra rodar umas bibliotecas do sistema)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copia dependências primeiro (cache inteligente)
COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copia o projeto inteiro
COPY . .

# Porta que o FastAPI usa
EXPOSE 8000

# Comando de inicialização para conteineir Docker
CMD ["gunicorn", "api.main:app", "-k", "uvicorn.workers.UvicornWorker", "-w", "4", "-b", "0.0.0.0:8000"]

# Comando de inicializção local/host
# CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
