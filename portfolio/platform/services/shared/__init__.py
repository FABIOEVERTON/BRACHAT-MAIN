"""Plataforma EZRA — Núcleo compartilhado (PRD §2.2 services/shared).

API pública para todos os serviços: config, chain hash, tipagem de laudo.
"""

from services.shared.config import SharedSettings, get_settings

__all__ = ["SharedSettings", "get_settings"]
__version__ = "0.1.0"