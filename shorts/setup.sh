#!/usr/bin/env bash
# Installiert die Werkzeuge für make_short.py (Ubuntu/Debian).
set -e
command -v espeak-ng >/dev/null && [ -d /usr/share/mbrola/de6 ] && exit 0
apt-get update -qq && apt-get install -y -qq ffmpeg espeak-ng mbrola-de6
python3 -c "import PIL" 2>/dev/null || pip3 install -q Pillow
