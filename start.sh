#!/usr/bin/env bash

# Instala Chromium y su driver
apt-get update
apt-get install -y chromium chromium-driver

# Exporta el path (por si Selenium lo necesita)
export CHROME_BIN=/usr/bin/chromium
export PATH=$PATH:/usr/bin

# Ejecuta tu aplicación
gunicorn app:app --bind 0.0.0.0:$PORT
