from db  import models, database
from sqlalchemy import insert, select, func
from loguru import logger
from get_token import get_token
import asyncio


async def save_cookie(data: dict, market_place: models.MarketPlace = models.MarketPlace.wildberries) :
    async with database.get_db() as session:
        query = insert(models.Cookie).values(source=market_place, **data)
        await session.execute(query)


async def cookie_count():
    async with database.get_db() as session:
        count_query = select(func.count()).select_from(models.Cookie).where(
            models.Cookie.source == models.MarketPlace.wildberries
        )
        count_result = await session.execute(count_query)
        current_count = count_result.scalar()
        return current_count


async def cookie_producer_loop():
    while True:
        current_count = await cookie_count()

        if current_count >= 10:
            logger.info(f"--> [C-MANAGER] База заполнена ({current_count}/10). Жду освобождения места...")
            await asyncio.sleep(20)
            continue

        logger.info(f"--> [C-MANAGER] Есть место для новой куки ({current_count}/10). Запускаю добычу...")

        try:
            new_cookie = await get_token()
            await save_cookie(new_cookie)
            logger.success("--> [C-MANAGER] Кука успешно добыта и сохранена.")
        except Exception as e:
            logger.error(f"--> [C-MANAGER] Ошибка при добыче: {e}")
            await asyncio.sleep(10)