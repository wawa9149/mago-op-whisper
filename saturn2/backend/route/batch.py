#!/usr/bin/env python
# encoding: utf-8
# Copyright (c) 2025- SATURN
# AUTHORS:
# Sukbong Kwon (Galois)

# Batch processing in the background

from pathlib import Path
from typing import Dict, Any, Callable, List
from fastapi import UploadFile
from fastapi.responses import JSONResponse

# Local
from .status import Status, set_status_path, update_status
from .upload import upload_file
from ..code.code import (
    MESSAGE_SUCCESS,
    ERROR_PROCESS_FAILED,
    ERROR_UPLOAD_FAILED,
)
from .wrapper import json_response_wrapper

async def run_batch(
    model: Callable[..., Any],
    file: UploadFile,
    content_id: str,
    out_dir: str,
    **kwargs,
)-> Dict:
    """Run batch processing on a single file.

    Args:
        model (Callable): The model to run.
        file (UploadFile): The file to process.
        content_id (str): The content ID.
        out_dir (str): The output directory.
        **kwargs: Additional arguments for the model.
    Returns:
        Dict: A dictionary containing the status of the processing.
    """
    try:
        content_id, status_path = set_status_path(content_id, out_dir)

        # Upload file
        file_path = str(Path(status_path).parent / Path(file.filename or "unknown").name)
        try:
            await upload_file(file, status_path, file_path)
        except Exception as e:
            return ERROR_UPLOAD_FAILED(content={"id": content_id, "detail": str(e)}).asdict()

        # Inference
        result = await inference(
            model,
            file_path,
            content_id,
            status_path,
            **kwargs,
        )
        return result
    except Exception as e:
        update_status(status_path, Status.FAILED, str(e))
        return ERROR_PROCESS_FAILED(content={"id": content_id, "error": str(e)}).asdict()

async def run_batch_files(
    model: Callable[..., Any],
    files: List[UploadFile],
    content_id: str,
    out_dir: str,
    **kwargs,
)-> Dict:
    """Run batch processing on multiple files.

    Args:
        model (Callable): The model to run.
        files (List[UploadFile]): List of files to process.
        content_id (str): The content ID.
        out_dir (str): The output directory.
        **kwargs: Additional arguments for the model.

    Returns:
        Dict: A dictionary containing the status of the processing.
    """
    content_id, status_path = set_status_path(content_id, out_dir)

    # Upload files
    file_paths = []
    for file in files:
        file_path = str(Path(status_path).parent / Path(file.filename or "unknown").name)
        try:
            await upload_file(file, status_path, file_path)
            file_paths.append(file_path)
        except Exception as e:
            return ERROR_UPLOAD_FAILED(content={"id": content_id, "detail": str(e)}).asdict()

    return await inference(
        model,
        file_paths,
        content_id,
        status_path,
        **kwargs
    )

async def run_batch_uri(
    model: Callable[..., Any],
    file_path: str,
    content_id: str,
    out_dir: str,
    **kwargs,
)-> Dict:
    """Run batch processing on a single URI.

    Args:
        model (Callable): The model to run.
        file_path (str): The path to the input file.
        content_id (str): The content ID.
        out_dir (str): The output directory.
        **kwargs: Additional arguments for the model.

    Returns:
        Dict: A dictionary containing the status of the processing.
    """
    content_id, status_path = set_status_path(content_id, out_dir)

    return await inference(
        model,
        file_path,
        content_id,
        status_path,
        **kwargs
    )

async def run_batch_uris(
    model: Callable[..., Any],
    file_paths: List[str],
    content_id: str,
    out_dir: str,
    **kwargs,
)-> Dict:
    """Run batch processing on multiple URIs.

    Args:
        model (Callable): The model to run.
        file_paths (List[str]): List of file paths to process.
        content_id (str): The content ID.
        out_dir (str): The output directory.
        **kwargs: Additional arguments for the model.

    Returns:
        Dict: A dictionary containing the status of the processing.
    """
    content_id, status_path = set_status_path(content_id, out_dir)

    return await inference(
        model,
        file_paths,
        content_id,
        status_path,
        **kwargs
    )

async def run_batch_bytes(
    model: Callable[..., Any],
    data: bytes,
    content_type: str,
    content_id: str,
    out_dir: str,
    **kwargs,
)-> Dict:
    """Run batch processing on a base64 encoded string.

    Args:
        model (Callable): The model to run.
        data (str): The base64 encoded string.
        content_id (str): The content ID.
        out_dir (str): The output directory.
        **kwargs: Additional arguments for the model.

    Returns:
        Dict: A dictionary containing the status of the processing.
    """
    # Set status path
    content_id, status_path = set_status_path(content_id, out_dir)

    # Get file suffix from content type
    suffix = content_type.split("/")[-1]

    # Save to data to speech file
    file_path = str(Path(status_path).with_suffix(f".{suffix}"))

    # Read raw bytes and save to file
    try:
        Path(file_path).write_bytes(data)
    except Exception as e:
        return ERROR_UPLOAD_FAILED(content={"id": content_id, "detail": str(e)}).asdict()

    print (f"Run batch bytes: {file_path}")

    return await inference(
        model,
        file_path,
        content_id,
        status_path,
        **kwargs
    )


@json_response_wrapper
async def inference(
    model: Callable[..., Any],
    file_path: str | List[str],
    content_id: str,
    status_path: str,
    **kwargs,
)-> Dict:
    """Run inference on a single file.
    Args:
        model (Callable): The model to run.
        file_path (str): The path to the input file.
        content_id (str): The content ID.
        status_path (str): The path to the status file.
        **kwargs: Additional arguments for the model.

    Returns:
        Dict: A dictionary containing the status of the inference.
    """
    detail = file_path if isinstance(file_path, str) else ','.join(file_path)

    # Update status to RUNNING
    update_status(status_path, Status.RUNNING, detail)

    # Inference with the model
    out_dir = str(Path(status_path).parent)
    result = model(file_path, out_dir=out_dir, content_id=content_id, **kwargs)

    # Update status to DONE
    update_status(status_path, Status.DONE, detail)

    # Return the result
    return MESSAGE_SUCCESS(content={"id": content_id, "result": result}).asdict()

