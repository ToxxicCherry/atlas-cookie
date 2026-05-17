from db import database, models, db_actions
import asyncio
import sys


if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

async def init_db():
    async with database.engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)

async def main():
    await init_db()
    await db_actions.cookie_producer_loop()


if __name__ == '__main__':
    asyncio.run(main())