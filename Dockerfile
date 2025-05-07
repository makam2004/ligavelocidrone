# Usa una imagen base ligera con Chrome
FROM python:3.11-slim

# Instala dependencias del sistema
RUN apt-get update && apt-get install -y \
    wget unzip curl gnupg \
    fonts-liberation libappindicator3-1 libasound2 \
    libatk-bridge2.0-0 libatk1.0-0 libcups2 libdbus-1-3 \
    libgdk-pixbuf2.0-0 libnspr4 libnss3 libx11-xcb1 \
    libxcomposite1 libxdamage1 libxrandr2 xdg-utils \
    libgbm1 libgtk-3-0 libxshmfence-dev \
    chromium chromium-driver \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Configura directorio de trabajo
WORKDIR /app

# Copia los archivos del proyecto
COPY . .

# Instala dependencias Python
RUN pip install --no-cache-dir -r requirements.txt

# Comando para iniciar Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:10000", "app:app"]
