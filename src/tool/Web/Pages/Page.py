from App.Objects.Object import Object
from App.Storage.Item.StorageItem import StorageItem
from Web.Pages.HTMLFile import HTMLFile
from Web.Pages.Assets.Asset import Asset
from Web.Pages.Assets.Favicon import Favicon
from Web.Pages.Assets.Meta import Meta
from typing import Any
from pydantic import Field
from App.Objects.Requirements.Requirement import Requirement
from Web.Pages.Crawler.Webdrivers.WebdriverPage import WebdriverPage

class Page(Object):
    _downloader: Any = None
    _page: WebdriverPage = None

    html: HTMLFile = Field(default = None)
    assets: list[Asset] = Field(default = None)
    favicons: list[Favicon] = Field(default = [])
    meta_tags: list[Meta] = Field(default = [])
    page_links: list = Field(default = [])
    url: str = Field(default = None)
    base_url: str = Field(default = None)
    relative_url: str = Field(default = None)

    _unserializable = ['_downloader', '_page']

    def get_html(self):
        return self.html

    def create_file(self, storage: StorageItem):
        storage_unit = storage.storage_adapter.get_storage_unit()
        link = self.link(storage_unit)

        self.html = HTMLFile()

        return self.html.create(storage_unit, link)

    def set_title(self, title: str):
        self.obj.name = title

    def get_html_file(self):
        return self.file.get_storage_unit()

    async def from_url(self, url: str):
        self._page = await self._downloader.webdriver.new_page()
        self.log('opened page, going to {0}'.format(url))

        await self._page.goto(url)

        self.log('opened url {0}'.format(url))

    async def set_info(self):
        self.set_title(await self._page.get_title())
        self.url = self._page.get_url(True)
        self.base_url = self._page.get_base_url()
        self.relative_url = await self._page.get_relative_url()

    # crawling methods

    def set_downloader(self, downloader):
        self._downloader = downloader

    async def clear(self):
        if self._page:
            await self._page.close()

        if self._downloader:
            await self._downloader.webdriver.clear()
            self._downloader = None

    @classmethod
    def _requirements(cls) -> list:
        return [
            Requirement(
                name = 'playwright',
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
