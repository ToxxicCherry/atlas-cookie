import time
import asyncio
from seleniumbase import Driver
from loguru import logger

BASE_URL = 'https://www.wildberries.ru'
test_url = 'http://ip-api.com/json/'
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36'
COOKIE_NEEDED = 'x_wbaas_token'

TIME_FOR_RETRY = 5


class WbCookies:
    def __init__(self, url: str = None, user_agent: str = None, cookie_needed: str = None, retry_delay: int = None):
        self.url = url or BASE_URL
        self.user_agent = user_agent or USER_AGENT
        self.cookie_needed = cookie_needed or COOKIE_NEEDED
        self.retry_delay = retry_delay or TIME_FOR_RETRY

    def get_token(self) -> dict | None:
        driver = Driver(
            uc=True,
            headed=False,
            headless=True,
            no_sandbox=True,
            agent=self.user_agent
        )

        driver.open(self.url)
        data = {}
        try:
            for i in range(3):
                logger.info(f'Попытка получить новые куки {i+1}')
                cookies = driver.execute_cdp_cmd('Network.getAllCookies', {})
                user_agent = driver.execute_script("return navigator.userAgent;")
                data['user_agent'] = user_agent

                for cookie in cookies.get('cookies'):
                    if cookie.get('name') == COOKIE_NEEDED:
                        logger.success(f'Нашел {self.cookie_needed}')
                        data[self.cookie_needed] = cookie.get('value')
                if self.cookie_needed in data and 'user_agent' in data:
                    return data
                time.sleep(self.retry_delay)
            else:
                logger.error('Куки не найдены')
                return None
        finally:
            driver.quit()


async def get_token() -> dict:
    token = await asyncio.to_thread(WbCookies().get_token)
    return token