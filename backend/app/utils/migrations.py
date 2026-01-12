import logging
import os
import subprocess
from pathlib import Path

logger = logging.getLogger("kitsu.migrations")


def run_migrations() -> None:
    logger.info("Running Alembic migrations…")

    project_root = Path(__file__).resolve().parent.parent.parent
    try:
        result = subprocess.run(
            ["alembic", "upgrade", "head"],
            capture_output=True,
            text=True,
            env=os.environ.copy(),
            cwd=project_root,
            timeout=60,
        )
    except subprocess.TimeoutExpired as exc:
        logger.error("Alembic migrations timed out after %s seconds", exc.timeout)
        raise RuntimeError("Alembic migrations timed out") from exc

    if result.returncode != 0:
        stderr = result.stderr.strip()
        logger.error("Alembic migrations failed:\n%s", stderr or "<no stderr>")
        raise RuntimeError("Alembic migrations failed")

    logger.info("Alembic migrations applied successfully")
