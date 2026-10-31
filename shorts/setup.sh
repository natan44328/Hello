#!/usr/bin/env bash
# Installiert alles für make_short.py (Ubuntu/Debian): ffmpeg, Piper-TTS, deutsche Stimme.
set -e
cd "$(dirname "$0")"
command -v ffmpeg >/dev/null || (apt-get update -qq && apt-get install -y -qq ffmpeg)
python3 -c "import piper" 2>/dev/null || pip3 install -q piper-tts
python3 -c "import PIL" 2>/dev/null || pip3 install -q Pillow
if [ ! -f voices/de-thorsten-low.onnx ]; then
  mkdir -p voices
  curl -sSL https://github.com/rhasspy/piper/releases/download/v0.0.2/voice-de-thorsten-low.tar.gz | tar -xz -C voices
fi
