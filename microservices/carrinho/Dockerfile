FROM python:3.11-slim

WORKDIR /app

# Copia requirements e instala dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia código da aplicação
COPY . .

# Expõe porta
EXPOSE 5002

# Variáveis de ambiente padrão
ENV FLASK_APP=app.py
ENV PORT=5002

# Comando de inicialização
CMD ["gunicorn", "--bind", "0.0.0.0:5002", "--workers", "4", "--timeout", "60", "app:app"]
