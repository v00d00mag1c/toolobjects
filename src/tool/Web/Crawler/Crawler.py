from App.Objects.Object import Object
from App.Objects.Arguments.Argument import Argument
from Data.String import String
from Data.Int import Int
from Data.Float import Float
from Web.Crawler.Webdrivers.Webdriver import Webdriver
from App.Objects.Requirements.Requirement import Requirement
from pydantic import Field
import asyncio

class Crawler(Object):
    webdriver: Webdriver = Field(default = None)

    async def start_webdriver(self):
        await self.webdriver.start()

    async def get_url(self, url: str):
        self.webdriver._driver.get(url)

        self.log('opened url {0}'.format(url))

        self.webdriver._driver.implicitly_wait(self.getOption('web.crawler.implicitly_wait'))

    async def scroll_down(self):
        last_height = self.webdriver._driver.execute_script('return document.body.scrollHeight')
        scroll_cycles = self.getOption('web.crawler.scroll_cycles')
        scroll_iter = 0

        while True:
            if scroll_cycles != None:
                if scroll_iter > scroll_cycles:
                    break

            self.webdriver._driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')

            self.log('scrolling down: {0}'.format(scroll_iter))

            await asyncio.sleep(self.getOption('web.crawler.scroll_timeout'))

            new_height = self.webdriver._driver.execute_script('return document.body.scrollHeight')
            if new_height == last_height:
                self.log('scrolling down: height is not updating')

                break

            last_height = new_height
            scroll_iter += 1

    @classmethod
    def _settings(cls):
        return [
            Argument(
                name = 'web.crawler.user_agent',
                default = None,
                orig = String
            ),
            Argument(
                name = 'web.crawler.scroll_cycles',
                default = None,
                orig = Int
            ),
            Argument(
                name = 'web.crawler.scroll_timeout',
                default = 1,
                orig = Float
            ),
            Argument(
                name = 'web.crawler.implicitly_wait',
                default = 5,
                orig = Int
            )
        ]

    @classmethod
    def _requirements(cls) -> list:
        return [
            Requirement(
                name = 'selenium',
                version = '4.39.0'
            ),
            Requirement(
                name = 'beautifulsoup4',
                version = '4.14.3'
            ),
            Requirement(
                name = 'ua-generator',
                version = '2.0.19'
            )
        ]
