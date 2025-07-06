#!/usr/bin/env python
# encoding: utf-8
# Copyright (c) 2025- SATURN
# AUTHORS:
# Sukbong Kwon (Galois)

import argparse
from pathlib import Path

VERSION = Path("VERSION").read_text().split("\n")[0]

def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description='Speech recognition with OpenAI whisper model',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        add_help=True,
    )

    parser.add_argument(
        'media',
        type=str,
        help='Path to media file: wav, mp3, mp4, flac, etc.'
    )

    parser.add_argument(
        '--version',
        action='version',
        version=VERSION,
        help='Show version and exit'
    )

    parser.add_argument(
        '--config',
        type=str,
        default='conf/config.yaml',
        help='Path to config file: yaml'
    )

    parser.add_argument(
        '--nocuda',
        action='store_true',
        help='Disable CUDA'
    )

    parser.add_argument(
        '--lang',
        type=str,
        default='Korean',
        help='Language code'
    )

    parser.add_argument(
        '-m', '--model-name', '--model_name',
        dest='model_name',
        type=str,
        default='medium',
        help='Model name of whisper, tiny, base, small, medium, large or turbo'
    )

    parser.add_argument(
        '-t', '--task',
        type=str,
        default='transcribe',
        help='Task name: transcribe / translate / all'
    )

    parser.add_argument(
        '-o', '--out-dir', '--out_dir',
        dest='out_dir',
        type=str,
        default='exp/whisper',
        help='Output directory'
    )

    parser.add_argument(
        '--model-root', '--model_root',
        dest='model_root',
        type=str,
        default='tiny',
        help='Model root directory'
    )

    return parser
