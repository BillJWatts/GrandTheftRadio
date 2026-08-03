# STAGE 1: Compile minimal FFmpeg
FROM debian:bookworm-slim AS builder

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    pkg-config \
    yasm \
    nasm \
    git \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /build
RUN git clone --depth 1 --branch n6.1.1 https://github.com/FFmpeg/FFmpeg.git ffmpeg

WORKDIR /build/ffmpeg

# Configure minimal ffmpeg build with only the required components.
RUN ./configure \
    --prefix=/build/out \
    --disable-everything \
    --disable-doc \
    --disable-ffplay \
    --disable-ffprobe \
    --disable-network \
    --disable-autodetect \
    --enable-ffmpeg \
    --enable-small \
    --enable-protocol=file,pipe \
    --enable-demuxer=mov,mp3,ogg,wav,pcm_s16le,s16le \
    --enable-muxer=s16le,pcm_s16le,opus,mp3 \
    --enable-decoder=h264,aac,mp3,opus,pcm_s16le \
    --enable-encoder=pcm_s16le,opus \
    --enable-parser=opus,mpegaudio \
    --enable-filter=volume,aresample,scale \
    && make -j$(nproc) \
    && make install

# STAGE 2: Python Runtime
FROM python:3.14-slim

COPY --from=builder /build/out/bin/ffmpeg /usr/local/bin/ffmpeg

RUN apt-get update && apt-get install -y --no-install-recommends \
    libopus0 \
    && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY . /app

ENV UV_NO_DEV=1

WORKDIR /app

RUN uv sync --frozen --no-cache

CMD ["uv", "run", "python", "src/main.py"]