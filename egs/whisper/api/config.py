#!/usr/bin/env python
# encoding: utf-8
# Copyright (c) 2025- SATURN
# AUTHORS:
# Sukbong Kwon (Galois)


APP_NAME = "WhisperAPI"
DESCRIPTION = "Speech recognition with OpenAI Whisper model"
COMPANY = "MAGO"
CONTACT = "galois@holamago.com"
APP_SYMBOL = "whisper"

try:
    from pathlib import Path
    _, VERSION, UPDATEDAT = Path("VERSION").read_text().split("\n")[0].strip().split('\t')
except Exception:
    VERSION = "N/A"
    UPDATEDAT = "N/A"
