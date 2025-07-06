#!/usr/bin/env python
# encoding: utf-8
# Copyright (c) 2025- SATURN
# AUTHORS:
# Sukbong Kwon (Galois)

from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class BaseResponse:
    """
    Standard response schema for API messages.
    """
    code: int
    message: str
    content: Dict[str, Any] = field(default_factory=dict)

    def asdict(self) -> Dict[str, Any]:
        """
        Convert the dataclass instance to a dictionary.
        """
        return {
            "code": self.code,
            "message": self.message,
            "content": self.content,
        }


# Success messages
@dataclass
class MESSAGE_SUCCESS(BaseResponse):
    code: int = 700
    message: str = "Success"

@dataclass
class MESSAGE_UPLOAD_SUCCESS(BaseResponse):
    code: int = 701
    message: str = "Upload success"

@dataclass
class MESSAGE_PROCESS_RUNNING(BaseResponse):
    code: int = 702
    message: str = "Process is running"

@dataclass
class MESSAGE_PROCESS_RUNNING_IN_THE_BACKGROUND(BaseResponse):
    code: int = 703
    message: str = "Process is running in the background"

@dataclass
class MESSAGE_PROCESS_DONE(BaseResponse):
    code: int = 704
    message: str = "Process is done"

@dataclass
class MESSAGE_PROCESS_NOT_YET_RUNNING(BaseResponse):
    code: int = 705
    message: str = "Process is not yet running"

@dataclass
class MESSAGE_PROCESS_PENDING(BaseResponse):
    code: int = 706
    message: str = "Process is pending"

@dataclass
class MESSAGE_PROCESS_WAITING(BaseResponse):
    code: int = 707
    message: str = "Process is waiting"


# Error messages
@dataclass
class ERROR_UNKNOWN(BaseResponse):
    code: int = 500
    message: str = "Unknown error"

@dataclass
class ERROR_PROCESS_FAILED(BaseResponse):
    code: int = 501
    message: str = "Process failed"

@dataclass
class ERROR_UPLOAD_FAILED(BaseResponse):
    code: int = 502
    message: str = "Upload failed"

@dataclass
class ERROR_SERVER_IS_BUSY(BaseResponse):
    code: int = 503
    message: str = "Server is busy"

@dataclass
class ERROR_INVALID_ID(BaseResponse):
    code: int = 510
    message: str = "Invalid ID"

@dataclass
class ERROR_INVALID_TASK(BaseResponse):
    code: int = 511
    message: str = "Invalid task"

@dataclass
class ERROR_INVALID_KEY(BaseResponse):
    code: int = 512
    message: str = "Invalid key"

@dataclass
class ERROR_FILE_NOT_FOUND(BaseResponse):
    code: int = 513
    message: str = "File not found"

@dataclass
class ERROR_INVALID_AUDIO(BaseResponse):
    code: int = 520
    message: str = "Invalid audio"

@dataclass
class ERROR_TASK_NOT_SUPPORTED(BaseResponse):
    code: int = 521
    message: str = "Task not supported"

@dataclass
class ERROR_INPUT_IS_EMPTY(BaseResponse):
    code: int = 522
    message: str = "Input is empty"
