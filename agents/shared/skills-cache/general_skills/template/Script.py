from __future__ import annotations

import argparse
import logging
import shutil
import subprocess
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Final, Iterator, NoReturn

# =============================================================================
# CUSTOM EXCEPTIONS (Specific. Never generic.)
# =============================================================================
class ValidationError(Exception): ...
class EnvironmentError(Exception): ...
class ExecutionError(Exception): ...

# =============================================================================
# CONFIGURATION (Immutable, type-safe data storage)
# =============================================================================
@dataclass(frozen=True)
class ScriptConfig:
    timeout: Final[int] = 30
    tool_name: Final[str] = "external-tool-cli"
    work_dir: Final[Path] = Path("/tmp/secure_profile")

# =============================================================================
# CONTEXT MANAGER (Safe setup & automatic cleanup)
# =============================================================================
@contextmanager
def managed_environment(config: ScriptConfig) -> Iterator[None]:
    config.work_dir.mkdir(parents=True, exist_ok=True)
    _inject_domain_logic(config.work_dir)  # AGNOSTIC: Place domain script here
    try:
        yield
    finally:
        shutil.rmtree(config.work_dir, ignore_errors=True)

# =============================================================================
# VALIDATION LAYER (Fail fast, clear messages)
# =============================================================================
def validate_input(file_path: Path, allowed_ext: str) -> None:
    if not file_path.is_file():
        raise FileNotFoundError(f"File missing: {file_path}")
    if file_path.suffix.lower() != allowed_ext:
        raise ValueError(f"Wrong format: {file_path.suffix}. Expected {allowed_ext}")

# =============================================================================
# EXECUTION LAYER (External tool wrapper)
# =============================================================================
def run_transformation(input_path: Path, output_path: Path, config: ScriptConfig) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(input_path, output_path)

    cmd = [config.tool_name, "--headless", f"--profile={config.work_dir}", str(output_path)]

    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True, timeout=config.timeout)
    except subprocess.TimeoutExpired as exc:
        raise ExecutionError(f"Timeout after {config.timeout}s") from exc
    except subprocess.CalledProcessError as exc:
        raise ExecutionError(f"Tool failed: {exc.stderr}") from exc

# =============================================================================
# POST-PROCESSING (Output guarantee)
# =============================================================================
def verify_output(file_path: Path) -> None:
    if not file_path.is_file() or file_path.stat().st_size == 0:
        raise FileNotFoundError("Output is empty or missing")
    # AGNOSTIC: Add domain-specific validation (e.g., schema, checksum)

# =============================================================================
# DOMAIN PLACEHOLDERS (Replace per skill)
# =============================================================================
def _inject_domain_logic(work_dir: Path) -> None:
    """AGNOSTIC: Insert macro/script/config required by the external tool."""
    pass

# =============================================================================
# ENTRY POINT (CLI + Orchestration)
# =============================================================================
def parse_cli() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Agnostic transformation script")
    parser.add_argument("input", type=Path, help="Source file path")
    parser.add_argument("output", type=Path, help="Destination file path")
    return parser.parse_args()

def main() -> NoReturn:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    args = parse_cli()
    config = ScriptConfig()

    try:
        validate_input(args.input, ".docx")
        with managed_environment(config):
            run_transformation(args.input, args.output, config)
        verify_output(args.output)
        logging.info("Done: %s → %s", args.input.name, args.output.name)
    except (FileNotFoundError, ValueError, EnvironmentError, ExecutionError) as err:
        logging.error("Failed: %s", err)
        raise SystemExit(1) from err
    except Exception as err:  # Fallback only for truly unexpected crashes
        logging.critical("Critical: %s", err)
        raise SystemExit(2) from err
    raise SystemExit(0)

if __name__ == "__main__":
    main()