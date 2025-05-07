#!/usr/bin/env bash
# exit on error
set -o errexit

STORAGE_DIR=/opt/render/project/.render

# Install dpkg if not already installed
if ! command -v dpkg &> /dev/null
then
  apt-get update && apt-get install -y dpkg
fi

# Download and install Google Chrome
if [[ ! -d $STORAGE_DIR/chrome ]]; then
  echo "...Downloading Chrome"
  mkdir -p $STORAGE_DIR/chrome
  cd $STORAGE_DIR/chrome
  wget -P ./ https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
  dpkg -x ./google-chrome-stable_current_amd64.deb $STORAGE_DIR/chrome
  rm ./google-chrome-stable_current_amd64.deb
  cd $HOME/project/src # Make sure we return to where we were
else
  echo "...Using Chrome from cache"
fi

# Download and install ChromeDriver
CHROMEDRIVER_VERSION=`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`
if [[ ! -d $STORAGE_DIR/chromedriver ]]; then
  echo "...Downloading ChromeDriver"
  mkdir -p $STORAGE_DIR/chromedriver
  cd $STORAGE_DIR/chromedriver
  wget -P ./ "https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip"
  unzip chromedriver_linux64.zip
  rm chromedriver_linux64.zip
  cd $HOME/project/src # Make sure we return to where we were
else
  echo "...Using ChromeDriver from cache"
fi

# Add Chrome and ChromeDriver's location to the PATH
export PATH="${PATH}:/opt/render/project/.render/chrome/opt/google/chrome"
export PATH="${PATH}:/opt/render/project/.render/chromedriver"

# add your own build commands...