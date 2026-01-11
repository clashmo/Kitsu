from logging import getLogger

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine

logger = getLogger(__name__)


async def check_database_connection(engine: AsyncEngine) -> None:
    async with engine.connect() as connection:
        await connection.execute(text("SELECT 1"))
