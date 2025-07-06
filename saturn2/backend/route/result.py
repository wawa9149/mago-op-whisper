#!/usr/bin/env python
# encoding: utf-8
# Copyright (c) 2025- SATURN
# AUTHORS:
# Sukbong Kwon (Galois)

from pathlib import Path
from typing import Dict, Any

from .status import Status, check_status
from ..code.code import (
    MESSAGE_SUCCESS,
    ERROR_PROCESS_FAILED,
)


def get_result(
    content_id: str,
    status_path: str,
) -> Dict[str, Any]:
    """
    Retrieve processing result or current status for the given content_id.

    Args:
        content_id (str): Unique ID of the content.
        status_path (str): Path to the .status file.

    Returns:
        Dict[str, Any]: Standard response dict.
    """
    path = Path(status_path)
    if not path.exists():
        return ERROR_PROCESS_FAILED(
            content={"id": content_id, "detail": "Status file not found."}
        ).asdict()

    raw = path.read_text(encoding="utf-8").strip().split("\t", 1)
    if len(raw) != 2:
        return ERROR_PROCESS_FAILED(
            content={"id": content_id, "detail": "Malformed status file."}
        ).asdict()

    status_str, result_path = raw
    try:
        status = Status(status_str)
    except ValueError:
        return ERROR_PROCESS_FAILED(
            content={"id": content_id, "detail": f"Unknown status '{status_str}'."}
        ).asdict()

    if status != Status.DONE:
        return check_status(content_id, status, result_path)

    result_file = Path(result_path)
    if not result_file.exists():
        return ERROR_PROCESS_FAILED(
            content={"id": content_id, "detail": "Result file not found."}
        ).asdict()

    return MESSAGE_SUCCESS(
        content={"id": content_id, "result": str(result_path)}
    ).asdict()
