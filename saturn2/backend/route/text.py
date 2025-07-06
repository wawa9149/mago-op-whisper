#!/usr/bin/env python
# encoding: utf-8
# Copyright (c) 2025- SATURN
# AUTHORS:
# Sukbong Kwon (Galois)

import inspect
from typing import Any, Callable
from fastapi.responses import JSONResponse

from ..code.code import MESSAGE_SUCCESS, ERROR_PROCESS_FAILED

async def run_text(
    model: Callable[..., Any],
    text: str,
    content_id: str,
    **kwargs,
) -> JSONResponse:
    """
    Execute text processing for a single input.
    Supports both synchronous and asynchronous model callables.
    Always returns a JSONResponse with a standardized success/error schema.
    """
    try:
        # Invoke the model (await if it's a coroutine, otherwise use directly)
        raw = model(text, content_id, **kwargs)
        if inspect.isawaitable(raw):
            raw = await raw

        # Build the success payload
        payload = MESSAGE_SUCCESS(
            content={"id": content_id, "result": raw}
        ).asdict()
        return JSONResponse(content=payload)

    except Exception as e:
        # Build the error payload (HTTP 500)
        error_payload = ERROR_PROCESS_FAILED(
            content={"id": content_id, "detail": str(e)}
        ).asdict()
        return JSONResponse(content=error_payload, status_code=500)
