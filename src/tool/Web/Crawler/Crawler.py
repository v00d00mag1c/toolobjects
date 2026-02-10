from App.Objects.Object import Object
from App.Objects.Arguments.ListArgument import ListArgument
from App.Objects.Arguments.Argument import Argument
from Data.Types.String import String
from Data.Types.Int import Int
from Data.Types.Float import Float
from Web.Crawler.Webdrivers.Webdriver import Webdriver
from App.Objects.Requirements.Requirement import Requirement
from Web.HTTP.Cookies import Cookies
from Web.Crawler.PageHTML import PageHTML
from urllib.parse import urlparse
from pydantic import Field
import asyncio


class Crawler(Object):
    webdriver: Webdriver = Field(default = None)
    url_override: str = Field(default = None)

    async def start_webdriver(self):
        await self.webdriver.start()

    async def set_url(self, url: str):
        self.log('opened url {0}'.format(url))

        self.webdriver._driver.get(url)
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

    def get_html(self):
        return self.webdriver._driver.page_source

    def get_parsed_html(self):
        return PageHTML.from_html(self.webdriver._driver.page_source)

    def get_title(self):
        return self.webdriver._driver.title

    def override_url(self, url: str):
        self.url_override = url

    def get_url(self):
        _url = self.url_override
        if _url == None:
            _url = self.webdriver._driver.current_url

        return urlparse(_url)

    def get_base_url(self):
        _url = self.get_url()
        return _url.scheme + '://' + _url.netloc

    def get_relative_url(self):
        _base_url = self.webdriver._driver.execute_script(f"return document.querySelector(\"base\") ? document.querySelector(\"base\").href : null")
        if _base_url == None:
            return self.get_base_url()

        return _base_url

    def set_cookies(self, items: list[Cookies] = []):
        for item in items:
            self.webdriver._driver.add_cookie(item.value)

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
            ),
            ListArgument(
                name = 'web.crawler.cookies',
                default = [],
                orig = Cookies
            ),
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
