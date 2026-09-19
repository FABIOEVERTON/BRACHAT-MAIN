"""Convenções obrigatórias (PRD §9.1).

create_service(name): FastAPI com CORS (ezra.com.br), /docs, /openapi.json, versão /v1.
Nenhum serviço pode pular este factory sem ADR (E0B-S01 F0B-01).
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from services.shared.api.deps import install_problem_handler


def create_service(name: str) -> FastAPI:
    app = FastAPI(
        title=f"EZRA — {name}",
        version="1.0.0",
        docs_url="/docs",
        openapi_url="/openapi.json",
    )

    install_problem_handler(app)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "https://ezra.com.br",
        ],
        allow_origin_regex=r"https://[a-z0-9-]+\.ezra\.com\.br",
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app