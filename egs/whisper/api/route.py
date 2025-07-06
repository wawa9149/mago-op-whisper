#!/usr/bin/env python
# encoding: utf-8
# Copyright (c) 2025- SATURN
# AUTHORS:
# Sukbong Kwon (Galois)

from pathlib import Path

from fastapi import (
    APIRouter,
    UploadFile,
    Depends,
    File,
    Body,
    Request,
    Query,
)
from fastapi.responses import JSONResponse, FileResponse

from saturn2.backend import (
    api_token,
    run_batch,
    run_batch_uri,
    run_batch_bytes,
)

# Local
from .model import model
from .config import APP_SYMBOL, VERSION, DESCRIPTION
from .body import RequestBody

# Define variables
EXP_FOLDER = Path("exp") / APP_SYMBOL
EXP_FOLDER.mkdir(parents=True, exist_ok=True)

# Define router
router = APIRouter(
    prefix=f"/{APP_SYMBOL}/v1",
    tags=[APP_SYMBOL],
    responses={404: {"description": "Not found"}},
)


##############################################
# API Endpoints
##############################################

@router.get(
    "/",
    summary="개요",
    description="OpenAI의 whisper를 사용한 음성인식 엔진 서비스입니다.",
    operation_id="overview_endpoint",
)
async def overview():
    """
    Overview of the API
    """
    return JSONResponse(
        content={
            "message": DESCRIPTION,
            "version": VERSION,
        }
    )

@router.post(
    "/run",
    summary="파일 업로드 방식",
    description="파일 업로드 방식으로 음성 파일을 전송하여 음성 파일을 텍스트로 변환합니다.",
    operation_id="run_endpoint", dependencies=[Depends(api_token)],
)
async def run(
    file: UploadFile = File(..., description="음성 파일을 업로드"),
    content_id: str = Body("", description="콘텐츠 아이디"),
    out_dir: str = Body(str(EXP_FOLDER), description="출력 디렉토리"),
    request_body: RequestBody = Depends(),
)-> dict:
    return await run_batch(
        model,
        file,
        content_id,
        out_dir,
        **request_body.model_dump(),
    )

@router.post(
    "/uri",
    summary="URI 방식",
    description="저장소에 있는 파일을 직접 사용하여 음성인식을 합니다.",
    operation_id="uri_endpoint",
    dependencies=[Depends(api_token)],
)
async def run_uri(
    uri: str = Body(..., description="저장소에 있는 파일의 URI"),
    content_id: str = Body("", description="콘텐츠 아이디"),
    out_dir: str = Body(str(EXP_FOLDER), description="출력 디렉토리"),
    request_body: RequestBody = Depends(),
)-> dict:
    return await run_batch_uri(
        model,
        uri,
        content_id,
        out_dir,
        **request_body.model_dump(),
    )

@router.post(
    "/bytes",
    summary="Binary 전송 방식",
    description="Binary 전송 방식으로 음성 파일을 전송하여 음성 파일을 텍스트로 변환합니다.",
    operation_id="bytes_endpoint",
    dependencies=[Depends(api_token)],
)
async def run_bytes(
    request: Request,
    data: bytes = Body(..., description="음성 파일의 바이트 데이터"),
    content_id: str = Query("", description="콘텐츠 아이디"),
    out_dir: str = Query(str(EXP_FOLDER), description="출력 디렉토리"),
    request_body: RequestBody = Depends(),
)-> dict:
    content_type = request.headers.get("content-type", "")
    return await run_batch_bytes(
        model,
        data,
        content_type,
        content_id,
        out_dir,
        **request_body.model_dump(),
    )


@router.get(
    "/download",
    summary="파일 다운로드",
    description="음성인식 결과 파일을 다운로드합니다.",
    operation_id="download_endpoint",
    dependencies=[Depends(api_token)],
)
async def download_file(
    file_path: str = Query(..., description="다운로드할 파일의 경로"),
):
    """Download result file

    Args:
        file_path (str): file path to download

    Returns:
        FileResponse: downloaded file
    """
    if not Path(file_path).exists():
        return JSONResponse(
            content={
                "message": "File not found",
            },
            status_code=404,
        )
    return FileResponse(file_path)