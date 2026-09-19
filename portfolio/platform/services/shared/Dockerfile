# Base para serviços Python (shared + produto na FASE 1+)
FROM python:3.13-slim AS base
WORKDIR /app
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 PIP_NO_CACHE_DIR=1
COPY services/shared ./services/shared
RUN pip install -e ./services/shared
COPY services ./services