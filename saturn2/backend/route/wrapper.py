# encoding: utf-8
# Copyright (c) 2025- SATURN
# AUTHORS:
# Sukbong Kwon (Galois)

from fastapi.responses import JSONResponse
from functools import wraps
from .status import Status, update_status
from ..code.code import (
    ERROR_PROCESS_FAILED,
)

def json_response_wrapper(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            result = await func(*args, **kwargs)
            return JSONResponse(result)
        except Exception as e:
            # content_id와 status_path가 kwargs에 있는 경우 처리
            content_id = kwargs.get("content_id", "unknown")
            status_path = kwargs.get("status_path")
            if status_path:
                update_status(status_path, Status.FAILED, str(e))

            return JSONResponse(
                ERROR_PROCESS_FAILED(content={"id": content_id, "error": str(e)}).asdict()
            )
    return wrapper