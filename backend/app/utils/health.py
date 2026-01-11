from logging import getLogger

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine

logger = getLogger(__name__)


async def check_database_connection(engine: AsyncEngine) -> None:
    """Check database connectivity by executing a simple SELECT 1.

    Raises:
        SQLAlchemyError: when the database is unreachable or the probe query fails.
    """
    async with engine.connect() as connection:
        await connection.execute(text("SELECT 1"))
