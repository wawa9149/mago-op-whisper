# ==================================================================
# Stage 1: Builder - Install Python packages into a venv
# ------------------------------------------------------------------
    FROM python:3.13-slim AS builder

    ENV VENV_PATH=/venv
    ENV PATH="$VENV_PATH/bin:$PATH"

    # 시스템 패키지 설치 (빌드용 의존성 포함)
    RUN apt-get update \
     && apt-get install -y --no-install-recommends \
          build-essential \
          git \
          curl \
          ffmpeg \
     && rm -rf /var/lib/apt/lists/*

    # 가상환경 생성 및 pip 업그레이드
    RUN python -m venv $VENV_PATH \
     && pip install --upgrade pip setuptools wheel

    # PyTorch (CPU) + torchaudio 설치
    RUN pip install --no-cache-dir \
          torch \
          torchaudio \
          --extra-index-url https://download.pytorch.org/whl/cpu

    # OpenAI whisper 설치 (GitHub 최신 버전)
    RUN pip install --no-cache-dir \
          git+https://github.com/openai/whisper.git

    # 프로젝트 의존성 설치
    # (호스트의 requirements.txt 위치에 맞춰 경로를 조정하세요)
    COPY egs/whisper/requirements.txt /deepsaturn/requirements.txt
    RUN pip install --no-cache-dir -r /deepsaturn/requirements.txt

# ==================================================================
# Stage 2: Runtime image
# ------------------------------------------------------------------
    FROM python:3.13-slim AS runtime

    ENV VENV_PATH=/venv
    ENV PATH="$VENV_PATH/bin:$PATH" \
        LC_ALL=C.UTF-8 \
        PYTHONUNBUFFERED=1 \
        PYTHONPATH="/deepsaturn:/deepsaturn/egs/whisper"

    # 최소 런타임 의존성만 설치 (ffmpeg 등)
    RUN apt-get update \
     && apt-get install -y --no-install-recommends \
          ffmpeg \
     && rm -rf /var/lib/apt/lists/*

    # 빌더에서 만든 가상환경 복사
    COPY --from=builder /venv /venv

    # 애플리케이션 코드 복사
    COPY saturn2 /deepsaturn/saturn2
    COPY egs      /deepsaturn/egs

    WORKDIR /deepsaturn/egs/whisper

    # 기본 실행 명령어 (필요에 따라 변경)
    CMD ["bash"]
