# Imagen oficial de Python
FROM python:3.11-slim

# Carpeta de trabajo
WORKDIR /app

# Copiamos requirements y los instalamos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos todo el código
COPY . .

# Comando para ejecutar el bot
CMD ["python", "bot.py"]
