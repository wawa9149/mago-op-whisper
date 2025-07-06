#!/usr/bin/env python
# encoding: utf-8
# Copyright (c) 2025- SATURN
# AUTHORS:
# Sukbong Kwon (Galois)

from pydantic import BaseModel, Field

class RequestBody(BaseModel):
    """
    Request body for the VAD API.
    """
    lang: str = Field(default="ko", description="언어")
    task: str = Field(default="transcribe", description="작업=transcribe/번역=translate")
