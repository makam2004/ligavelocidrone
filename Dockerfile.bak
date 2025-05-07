# Usa una imagen base de Python
FROM python:3.11-slim

# Actualiza los paquetes e instala dependencias de Chrome
RUN apt-get update \
    && apt-get install -y \
    wget \
    curl \
    gnupg2 \
    unzip \
    ca-certificates \
    && curl -sSL https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -o google-chrome.deb \
    && dpkg -i google-chrome.deb \
    && apt-get install -f -y

# Instala ChromeDriver
RUN curl -sSL https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip -o chromedriver.zip \
    && unzip chromedriver.zip -d /usr/local/bin/ \
    && chmod +x /usr/local/bin/chromedriver

# Instala dependencias de Python
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia el código fuente de la aplicación
COPY . .

# Expón el puerto en el que la aplicación correrá
EXPOSE 5000

# Comando para ejecutar la aplicación
CMD ["python", "app.py"]
