# ==========================================
# STAGE 1: Compile custom minimal FFmpeg
# ==========================================
FROM debian:bookworm-slim AS builder

# Install build essential dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    pkg-config \
    yasm \
    nasm \
    git \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Clone FFmpeg (pin to a stable version)
WORKDIR /build
RUN git clone --depth 1 --branch n6.1.1 https://github.com/FFmpeg/FFmpeg.git ffmpeg

WORKDIR /build/ffmpeg

# Configure minimal build
# Adjust --enable-* flags to fit your specific application needs!
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
    --enable-protocol=file \
    --enable-demuxer=mov,mp3 \
    --enable-decoder=h264,aac,mp3 \
    --enable-encoder=mp3,rawvideo \
    --enable-muxer=mp3,mp4 \
    --enable-filter=scale \
    && make -j$(nproc) \
    && make install

# ==========================================
# STAGE 2: Minimal Python Runtime
# ==========================================
FROM python:3.14-slim

# Copy the custom ~15MB binary from builder stage
COPY --from=builder /build/out/bin/ffmpeg /usr/local/bin/ffmpeg

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY . /app

ENV UV_NO_DEV=1

WORKDIR /app

RUN uv sync --frozen --no-cache

CMD ["uv", "run", "python", "src/main.py"]