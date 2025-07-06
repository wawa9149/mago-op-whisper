#!/usr/bin/env python
# encoding: utf-8
# Copyright (c) 2025- SATURN
# AUTHORS:
# Sukbong Kwon (Galois)

import torchaudio
from dataclasses import asdict
from pathlib import Path
from typing import Dict
from .schema import AudioInfo

def get_audio_info(
    audio: str,
)-> Dict:
    """Get audio information

    Args:
        audio (str): Path to the audio file
    Returns:
        Dict: Dictionary containing audio information
    """
    path = Path(audio)
    if not path.exists():
        return asdict(AudioInfo())

    try:
        info = torchaudio.info(audio)
        audio_info = AudioInfo(
            duration=info.num_frames / info.sample_rate,
            sample_rate=info.sample_rate,
            channels=info.num_channels,
        )
    except Exception:
        audio_info = AudioInfo()

    return asdict(audio_info)


