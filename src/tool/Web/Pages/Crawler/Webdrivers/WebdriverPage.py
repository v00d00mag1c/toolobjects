from App.Objects.Object import Object
from typing import Any
from urllib.parse import urlparse
import asyncio

class WebdriverPage(Object):
    url_override: str = None
    _page: Any = None
    _unserializable = ['_page']

    async def setViewport(self, viewport: dict):
        await self._page.set_viewport_size(viewport)

    async def goto(self, url: str, wait_until: str = 'domcontentloaded'):
        await self._page.goto(url, wait_until = wait_until)
        #page.wait_for_load_state('networkidle')

    async def close(self):
        await self._page.close()

    async def get_title(self):
        return await self._page.title()

    async def get_html(self):
        return await self._page.content()

    async def get_parsed_html(self):
        return None

    def get_url(self, orig: bool = False):
        _url = self.url_override
        if _url == None:
            _url = self._page.url

        if orig is True:
            return _url

        return urlparse(_url)

    def get_base_url(self):
        _url = self.get_url()
        return _url.scheme + '://' + _url.netloc

    async def get_relative_url(self):
        _base_url = await self._page.evaluate("""
                                              () => {return document.querySelector(\"base\") ? document.querySelector(\"base\").href : null}
                                              """)
        if _base_url == None:
            return self.get_base_url()

        return _base_url

    def override_url(self, url: str):
        self.url_override = url

    async def scroll_down(self, scroll_cycles: int = 10, scroll_timeout: int = 0):
        last_height = await self._page.evaluate('() => {return document.body.scrollHeight}')
        scroll_iter = 0

        while True:
            if scroll_cycles != None:
                if scroll_iter > scroll_cycles:
                    break

            await self._page.evaluate('() => window.scrollTo(0, document.body.scrollHeight);')

            self.log('scrolling down: {0}'.format(scroll_iter))

            await asyncio.sleep(scroll_timeout)

            new_height = await self._page.evaluate('() => {return document.body.scrollHeight}')
            if new_height == last_height:
                self.log('scrolling down: height is not updating')

                break

            last_height = new_height
            scroll_iter += 1

    def get(self):
        return self._page
