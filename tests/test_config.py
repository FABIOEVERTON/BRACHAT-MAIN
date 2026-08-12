"""Testes de configuração e validação básica."""
import os
import sys
from pathlib import Path

import pytest


def test_python_version():
    """Verifica se Python >= 3.11."""
    assert sys.version_info >= (3, 11), "Python 3.11+ requerido"


def test_project_structure():
    """Verifica estrutura básica do projeto."""
    root = Path(__file__).parent.parent
    assert (root / "portfolio").exists()
    assert (root / "portfolio" / "ezra_curator").exists()
    assert (root / "portfolio" / "ezra_curator" / "app").exists()
    assert (root / "requirements.txt").exists()


def test_env_example_exists():
    """Verifica se .env.example existe."""
    root = Path(__file__).parent.parent
    assert (root / ".env.example").exists()


def test_gitignore_exists():
    """Verifica se .gitignore existe."""
    root = Path(__file__).parent.parent
    assert (root / ".gitignore").exists()


def test_no_secrets_in_repo():
    """Verifica se não há segredos hardcoded no código."""
    import re
    root = Path(__file__).parent.parent
    secret_patterns = [
        r"sk-[a-zA-Z0-9]{32,}",
        r"gh[pousr]_[A-Za-z0-9]{36,}",
        r"x-consumer-api-key",
        r"password\s*=\s*['\"][^'\"]+['\"]",
        r"secret\s*=\s*['\"][^'\"]+['\"]",
        r"api_key\s*=\s*['\"][^'\"]+['\"]",
    ]
    for py_file in root.rglob("*.py"):
        if ".venv" in str(py_file) or "venv" in str(py_file) or "__pycache__" in str(py_file):
            continue
        content = py_file.read_text(encoding="utf-8")
        for pattern in secret_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            assert not matches, f"Possível segredo encontrado em {py_file}: {pattern}"


def test_requirements_exist():
    """Verifica se requirements.txt existe."""
    root = Path(__file__).parent.parent
    assert (root / "requirements.txt").exists()
    assert (root / "portfolio" / "ezra_curator" / "requirements.txt").exists()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])