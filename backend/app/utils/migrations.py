import logging
import os
import subprocess
from pathlib import Path

logger = logging.getLogger("kitsu.migrations")
PROJECT_ROOT = Path(__file__).resolve().parents[2]


def run_migrations() -> None:
    logger.info("Running Alembic migrations…")

    try:
        result = subprocess.run(
            ["alembic", "upgrade", "head"],
            capture_output=True,
            text=True,
            env=os.environ.copy(),
            cwd=PROJECT_ROOT,
            timeout=60,
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
