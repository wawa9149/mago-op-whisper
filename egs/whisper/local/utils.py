#!/usr/bin/env python
# encoding: utf-8
# Copyright (c) 2024- SATURN
# AUTHORS:
# Sukbong Kwon (Galois)

import json
from typing import Text

def format_timestamp(seconds) -> Text:
    """Convert seconds to SRT timestamp format (HH:MM:SS,ms)"""
    milliseconds = int((seconds - int(seconds)) * 1000)
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"

def format_vtt_timestamp(seconds) -> Text:
    """Convert seconds to VTT timestamp format (HH:MM:SS.ms)"""
    milliseconds = int((seconds - int(seconds)) * 1000)
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}.{milliseconds:03}"

def result2script(result) -> Text:
    """Convert the result to script format"""
    script = []
    for item in result.get("segments", []):
        script.append(item["text"].strip())
    return "\n".join(script)

def result2srt(result, path, start_time=0) -> None:
    """Convert the result to SRT format"""
    with open(path, "w", encoding="utf-8") as f:
        for i, item in enumerate(result.get("segments", [])):
            start = format_timestamp(start_time + item["start"])
            end = format_timestamp(start_time + item["end"])
            f.write(f"{i+1}\n{start} --> {end}\n{item['text'].strip()}\n\n")

def result2vtt(result, path, start_time=0) -> None:
    """Convert the result to VTT format"""
    with open(path, "w", encoding="utf-8") as f:
        f.write("WEBVTT\n\n")
        for i, item in enumerate(result.get("segments", [])):
            start = format_vtt_timestamp(start_time + item["start"])
            end = format_vtt_timestamp(start_time + item["end"])
            f.write(f"{i+1}\n{start} --> {end}\n{item['text'].strip()}\n\n")

def result2json(result, path) -> None:
    """Save JSON format to file"""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)