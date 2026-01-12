import logging
import os
import shutil
import subprocess
from pathlib import Path

logger = logging.getLogger("kitsu.migrations")


def _find_project_root() -> Path:
    current = Path(__file__).resolve()
    for parent in current.parents:
        if (parent / "alembic.ini").exists():
            return parent
    return current.parents[2]


# utils/migrations.py -> app -> backend -> project root (alembic.ini lives here)
PROJECT_ROOT = _find_project_root()
DEFAULT_TIMEOUT_SECONDS = 60
try:
    MIGRATIONS_TIMEOUT = int(os.getenv("ALEMBIC_TIMEOUT_SECONDS", DEFAULT_TIMEOUT_SECONDS))
except ValueError:
    MIGRATIONS_TIMEOUT = DEFAULT_TIMEOUT_SECONDS


def run_migrations() -> None:
    logger.info("Running Alembic migrations…")

    alembic_executable = shutil.which("alembic")
    if not alembic_executable:
        logger.error("Alembic executable not found in PATH")
        raise RuntimeError("Alembic executable not found")

    try:
        result = subprocess.run(
            [alembic_executable, "upgrade", "head"],
            capture_output=True,
            text=True,
            env=os.environ.copy(),
            cwd=PROJECT_ROOT,
            timeout=MIGRATIONS_TIMEOUT,
        )
    except subprocess.TimeoutExpired as exc:
        logger.error("Alembic migrations timed out after %s seconds", exc.timeout)
        raise RuntimeError("Alembic migrations timed out") from exc

    if result.returncode != 0:
        stderr = result.stderr.strip()
        logger.error("Alembic migrations failed:\n%s", stderr or "<no stderr>")
        stdout = result.stdout.strip()
        if stdout:
            logger.error("Alembic migrations stdout:\n%s", stdout)
        raise RuntimeError("Alembic migrations failed")

    logger.info("Alembic migrations applied successfully")
