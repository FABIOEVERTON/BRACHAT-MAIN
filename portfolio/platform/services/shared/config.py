"""Configuração compartilhada dos serviços (PRD §2.2 services/shared).

Settings base via pydantic-settings — carregada por todos os serviços.
Env prefix: EZRA_  (ex: EZRA_DB_URL, EZRA_ENV).
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class SharedSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="EZRA_", env_file=".env", extra="ignore")

    env: str = "development"  # development | staging | production
    db_url: str = "postgresql+asyncpg://ezra:ezra@localhost:5432/ezra"
    redis_url: str = "redis://localhost:6379/0"
    aws_region: str = "sa-east-1"  # ADR-008: soberania de dados
    log_level: str = "INFO"


def get_settings() -> SharedSettings:
    return SharedSettings()