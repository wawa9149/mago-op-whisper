#!/usr/bin/env python
# encoding: utf-8
# Copyright (c) 2025- SATURN
# AUTHORS:
# Sukbong Kwon (Galois)

from local.transcribe import Whisper

model = Whisper.from_config_yaml(
    config_yaml="conf/config.yaml",
)

