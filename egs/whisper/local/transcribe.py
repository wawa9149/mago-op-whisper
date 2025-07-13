#!/usr/bin/env python
# encoding: utf-8
# Copyright (c) 2025- SATURN
# AUTHORS:
# Sukbong Kwon (Galois)

import yaml
import torch
import whisper
import uuid
from pathlib import Path
from pydantic import BaseModel, Field
from typing import Any, Dict

# Saturn2
from saturn2.utils.logs import get_logger
from saturn2.media.helper.inspect_audio import get_audio_info
from saturn2.helper.decorators import decoding_time_decorator

# Local
from local.utils import result2srt, result2vtt, result2json, result2script
from local.langmap import whisper_supported_languages

# Define
logger = get_logger(__name__, level="INFO")

class WhisperConfig(BaseModel):
    whisper_model: Any = None
    device: str = Field(
        default="cuda" if torch.cuda.is_available() else "cpu",
        description="Device to use for the model",
    )
    out_dir: str = Field(
        default="exp",
        description="Output directory to save processed files",
    )
    lang: str = Field(
        default="auto",
        description="Language to use for the model",
    )
    task: str = Field(
        default="transcribe",
        description="Task to perform, transcribe or translate",
    )
    decoding_options: Dict = Field(
        default={},
        description="Decoding options for the model",
    )

class Whisper(WhisperConfig):
    """Speech recognition with OpenAI whisper model (`Whisper`)
    """
    def __init__(
        self,
        model_name: str = "medium",
        nocuda: bool = False,
        **kwargs,
    )-> None:
        """Initialize the Whisper instance
        Args:
            model_name (str, optional): Model name of whisper, tiny, base, small, medium, large or turbo. Defaults to "turbo".
            nocuda (bool, optional): Disable CUDA. Defaults to False.
            **kwargs: Additional arguments for the WhisperConfig class.
        """
        super().__init__(**kwargs)

        # Set device
        self.device = "cuda" if torch.cuda.is_available() and not nocuda else "cpu"
        logger.info(f"Device: {self.device}")

        # Check if model_root is provided
        model_root = kwargs.get("model_root", "")
        if model_root == "":
            model_path = model_name
        else:
            model_path = f"{model_root}/{model_name}.pt"

        self.whisper_model = whisper.load_model(model_path) # type: ignore
        logger.info(f"Model loaded: {model_path}")

        # Convert model to FP32 precision if device is CPU
        if self.device == "cpu":
            self.whisper_model = self.whisper_model.to(torch.float32)
            logger.info("Converted Whisper model to FP32 precision")

        # Set decoding options for the model
        self.decoding_options = whisper.DecodingOptions(language=self.lang, fp16=False) # type: ignore
        logger.info(f"Decoding options: {self.decoding_options}")

    @classmethod
    def from_config_yaml(
        cls,
        config_yaml: str
    )-> 'Whisper':
        """Form configuration yml

        Args:
            config_yaml (str): Path to the configuration yml file.
        """
        return cls(**yaml.safe_load(open(config_yaml, "r", encoding="utf-8")))

    @decoding_time_decorator
    def __call__(
        self,
        audio_path: str,
        content_id: str = "",
        out_dir: str = "",
        task: str = "",
        lang: str = "",
    )-> Dict:
        """Speech recognition with OpenAI whisper model

        Args:
            audio_path (str): Audio file path
            content_id (str): Content ID
            out_dir (str): Output directory to save temporary files
            task (str, optional): Task name. Defaults to "".
            lang (str, optional): Language code. Defaults to "".
        """
        logger.info(f"Transcribe audio: {audio_path}")

        # Set variables
        lang = lang or self.lang
        out_dir = out_dir or self.out_dir
        task = task or self.task

        # Check if language is supported by whisper
        if lang not in whisper_supported_languages:
            raise ValueError(f"Language {lang} is not supported by whisper")

        logger.info(f"Lang: {lang}, Out dir: {out_dir}, Task: {task}")

        # Set task list if task is "all" else set task list to [task]
        task_list = ["transcribe", "translate"] if task == "all" else [task]
        logger.info(f"Running {', '.join(task_list)} on: {audio_path}")

        # Get audio info
        result: Dict[str, Any] = {"audio_info": get_audio_info(audio_path)}

        # Set content_id if not provided
        content_id = content_id or str(uuid.uuid4())

        # Transcribe audio (translate is optional)
        for t in task_list:
            result[lang] = self.transcribe(
                audio_path=audio_path,
                content_id=content_id,
                out_dir=out_dir,
                task=t,
                lang=lang,
            )

        logger.info(f"Transcription completed: {audio_path}")

        return result

    def transcribe(
        self,
        audio_path: str,
        content_id: str,
        out_dir: str,
        task: str,
        lang: str,
    )-> Dict:
        """Transcribe audio_path with OpenAI whisper model

        Args:
            audio_path   (str): Path to the audio file.
            content_id (str): Content ID
            out_dir (str): Base output directory.
            task    (str): 'transcribe' or 'translate'.
            lang    (str): Language code to decode in (e.g. 'ko', 'en', 'fr', ...).

        Returns:
            Dict: Recognition result
        """
        # SETP 1: Run whisper
        # if lang is "auto", using lang detection
        if lang == "auto":
            result = self.whisper_model.transcribe(
                audio_path,
                task=task,
                **({} if self.device == "cuda" else {"fp16": False})
            )
        else:
            result = self.whisper_model.transcribe(
                audio_path,
                language=lang,
                task=task,
                **({} if self.device == "cuda" else {"fp16": False})
            )

        # SETP 2: Prepare language-specific output folder
        folder = Path(out_dir) / lang / content_id
        folder.mkdir(parents=True, exist_ok=True)

        # SETP 3: Define the save path
        stem = Path(audio_path).stem
        json_path = folder / f"{stem}.json"
        srt_path = folder / f"{stem}.srt"
        vtt_path = folder / f"{stem}.vtt"

        # SETP 4: Save the result
        result2json(result, json_path)
        result2srt(result, srt_path)
        result2vtt(result, vtt_path)
        result.update({
            "json_path": str(json_path),
            "srt": str(srt_path),
            "vtt": str(vtt_path),
            "script": result2script(result),
        })

        # Remove `segments` key if it is not necessary
        if "segments" in result:
            result.pop("segments")

        return result


def main():
    import json
    from local.parser import get_parser
    args = get_parser().parse_args()

    # app = Whisper.from_config_yaml(
    #     config_yaml=args.config,
    # )

    app = Whisper(**vars(args))

    result = app(
        audio_path=args.media,
        content_id="",
        out_dir=args.out_dir,
        task=args.task,
        lang=args.lang,
    )
    print(json.dumps(result, indent=4, ensure_ascii=False))

if __name__ == '__main__':
    main()