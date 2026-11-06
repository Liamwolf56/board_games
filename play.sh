#!/bin/bash
cd "$(dirname "$0")"
if [ "$(uname)" = "Darwin" ]; then APP="app/macos-latest/main_hub/main_hub"; else APP="app/ubuntu-latest/main_hub/main_hub"; fi
if [ -f "$APP" ]; then chmod +x "$APP"; "$APP"; else python3 main_hub.py; fi
