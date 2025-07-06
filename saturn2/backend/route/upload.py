#!/usr/bin/env python
# encoding: utf-8
# Copyright (c) 2025- SATURN
# AUTHORS:
# Sukbong Kwon (Galois)

import aiofiles
from pathlib import Path
from typing import Dict
from fastapi import UploadFile

from .status import Status
from ..code.code import MESSAGE_UPLOAD_SUCCESS


async def upload_file(
    file: UploadFile,
    status_path: str,
    file_path: str,
)-> Dict:
    """
    Save an UploadFile to disk under out_dir/<id>/ and update its status file.

    Args:
        file (UploadFile): The file to upload.
        status_path (str): The path to the status file.
        file_path (str): The path of the uploaded file.
    Returns:
        Dict: A dictionary containing the status of the upload.
        (empty dictionary if successful, or an error message if failed)
    """
    try:
        # 비동기로 저장
        async with aiofiles.open(file_path, "wb") as buffer:
            while chunk := await file.read(1024 * 1024):
                await buffer.write(chunk)

        # Update the status file
        Path(status_path).write_text(
            '\t'.join([
                Status.UPLOADED.value,
                f"File {file.filename} uploaded successfully",
            ])
        )
        return MESSAGE_UPLOAD_SUCCESS(content={"id": file_path}).asdict()
    except Exception as e:
        # If the upload fails, update the status file with the error message
        Path(status_path).write_text(
            '\t'.join([
                Status.FAILED.value,
                f"File {file.filename} upload failed: {str(e)}",
            ])
        )
        raise RuntimeError(str(e))


