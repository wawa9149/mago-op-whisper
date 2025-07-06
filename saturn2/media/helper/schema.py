#!/usr/bin/env python
# encoding: utf-8
# Copyright (c) 2025- SATURN
# AUTHORS:
# Sukbong Kwon (Galois)


from dataclasses import dataclass


@dataclass
class AudioInfo:
    """Audio information
    """
    duration: float = 0.0
    sample_rate: int = 0
    channels: int = 0

    def __post_init__(self):
        self.duration = round(self.duration, 3)