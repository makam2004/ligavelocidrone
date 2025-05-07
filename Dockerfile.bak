# Usa una imagen base ligera de Python
FROM python:3.11-slim

# Instala dependencias del sistema
RUN apt-get update && apt-get install -y \
    wget unzip curl gnupg2 fonts-liberation \
    libasound2 libatk1.0-0 libatk-bridge2.0-0 libcups2 \
    libdbus-1-3 libgdk-pixbuf2.0-0 libnspr4 libnss3 \
    libx11-xcb1 libxcomposite1 libxdamage1 libxrandr2 \
    libu2f-udev libvulkan1 libxss1 libxtst6 xdg-utils \
    --no-install-recommends

# Instala Google Chrome
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt install -y ./google-chrome-stable_current_amd64.deb && \
    rm google-chrome-stable_current_amd64.deb

# Crea una carpeta para la app
WORKDIR /app

# Copia los archivos
COPY . .

# Instala las dependencias de Python
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expón el puerto
EXPOSE 10000

# Comando para ejecutar tu app
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:10000"]
