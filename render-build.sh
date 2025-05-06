#!/usr/bin/env bash
# Script que se ejecuta en Render antes de iniciar la app

# Instala Chromium
apt-get update && apt-get install -y chromium-browser chromium-chromedriver

# Mueve los binarios a una ruta conocida
ln -s /usr/bin/chromedriver /usr/local/bin/chromedriver
ln -s /usr/bin/chromium-browser /usr/local/bin/chrome
