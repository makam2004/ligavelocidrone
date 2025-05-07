#!/bin/bash
set -ex

# Instala Chromium desde el repositorio estándar
apt-get update
apt-get install -y chromium-browser

# Asegura que los enlaces simbólicos existan
ln -sf /usr/bin/chromium-browser /usr/bin/chromium
ln -sf /usr/bin/chromium-browser /usr/bin/google-chrome