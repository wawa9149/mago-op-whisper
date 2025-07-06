#!/usr/bin/env python
# encoding: utf-8
# Copyright (c) 2025- SATURN
# AUTHORS:
# Sukbong Kwon (Galois)

import uuid
from enum import Enum
from pathlib import Path
from typing import Dict, Any, Tuple

from ..code.code import (
    MESSAGE_UPLOAD_SUCCESS,
    MESSAGE_PROCESS_PENDING,
    MESSAGE_PROCESS_RUNNING_IN_THE_BACKGROUND,
    MESSAGE_PROCESS_WAITING,
    MESSAGE_PROCESS_DONE,
    ERROR_PROCESS_FAILED,
    ERROR_INVALID_TASK,
)

class Status(Enum):
    READY    = "READY"
    UPLOADED = "UPLOADED"
    PENDING  = "PENDING"
    RUNNING  = "RUNNING"
    WAITING  = "WAITING"
    DONE     = "DONE"
    FAILED   = "FAILED"


# Map each status to its handler and message template
_STATUS_MAP = {
    Status.UPLOADED: (
        MESSAGE_UPLOAD_SUCCESS,
        "File {content_id} uploaded successfully",
    ),
    Status.PENDING: (
        MESSAGE_PROCESS_PENDING,
        "File {content_id} pending processing",
    ),
    Status.RUNNING: (
        MESSAGE_PROCESS_RUNNING_IN_THE_BACKGROUND,
        "File {content_id} is being processed",
    ),
    Status.WAITING: (
        MESSAGE_PROCESS_WAITING,
        "File {content_id} is waiting for processing",
    ),
    Status.DONE: (
        MESSAGE_PROCESS_DONE,
        "File {content_id} processed successfully",
    ),
    Status.FAILED: (
        ERROR_PROCESS_FAILED,
        "{detail}",
    ),
}

def check_status(
    content_id: str,
    status: Status,
    detail: str = "",
) -> Dict:
    """
    Return a standardized status response based on current processing status.

    Args:
        content_id (str): Unique identifier for the content.
        status (Status): Current status of the content.
        detail (str): Additional detail message for the status.

    Returns:
        Dict: A dictionary containing the status response.

    >>> check_status("12345", Status.UPLOADED)
    {'code': 701, 'message': 'Upload success', 'content': {'content_id': '12345', 'detail': 'File 12345 uploaded successfully'}}
    """
    handler, template = _STATUS_MAP.get(
        status,
        (ERROR_INVALID_TASK, f"File {content_id} has invalid status"),
    )
    message = handler(
        content={
            "content_id": content_id,
            "detail": template.format(content_id=content_id, detail=detail),
        }
    )
    return message.asdict()


def set_status_path(
    content_id: str,
    out_dir: str,
)-> Tuple[str, str]:
    """
    Create a status file under out_dir/<content_id>/<content_id>.status
    and initialize it to READY.

    Args:
        content_id (str): Unique identifier for the content.
        out_dir (str): Output directory where the status file will be created.
    Returns:
        str: Path to the status file.
    """
    if not content_id:
        content_id = uuid.uuid4().hex
    status_path = Path(out_dir) / content_id / f"{content_id}.status"
    status_path.parent.mkdir(parents=True, exist_ok=True)
    status_path.write_text(
        '\t'.join([
            Status.READY.value,
            f"{content_id} ready for processing",
        ]),
    )
    return content_id, str(status_path)


def update_status(status_path: str, status: Status, detail: Any) -> None:
    """Write the current status and detail to the status file.
    """
    Path(status_path).write_text(f"{status.value}\t{detail}", encoding='utf-8')