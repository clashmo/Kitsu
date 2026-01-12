import logging
import os
import subprocess
from pathlib import Path

logger = logging.getLogger("kitsu.migrations")


def run_migrations() -> None:
    logger.info("Running Alembic migrations…")

    result = subprocess.run(
        ["alembic", "upgrade", "head"],
        capture_output=True,
        text=True,
        env=os.environ.copy(),
        cwd=Path(__file__).resolve().parents[2],
    )

    if result.returncode != 0:
        stderr = result.stderr.strip()
        logger.error("Alembic migrations failed:\n%s", stderr or "<no stderr>")
        raise RuntimeError("Alembic migrations failed")

    logger.info("Alembic migrations applied successfully")
