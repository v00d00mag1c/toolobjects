from App.Objects.Object import Object
from App.Storage.Item.StorageItem import StorageItem
from Web.Pages.HTMLFile import HTMLFile
from Web.Pages.Assets.Asset import Asset
from Web.Pages.Assets.Media import Media
from Web.Pages.Assets.Favicon import Favicon
from Web.Pages.Assets.Meta import Meta
from Web.Pages.Assets.Link import Link
from Web.Pages.Assets.URL import URL
from typing import Any
from pydantic import Field
from App.Objects.Requirements.Requirement import Requirement
from Web.Pages.Crawler.Webdrivers.WebdriverPage import WebdriverPage
from App.Objects.Operations.Create.CreationItem import CreationItem

class Page(Object):
    _downloader: Any = None
    _crawler: Any = None
    _page: WebdriverPage = None
    _page_response: Any = None

    html: HTMLFile = Field(default = None)
    assets: list[Asset] = Field(default = None)
    favicons: list[Favicon] = Field(default = [])
    meta_tags: list[Meta] = Field(default = [])
    page_links: list[URL] = Field(default = [])
    media: list[Media] = Field(default = [])
    header_links: list[Link] = Field(default = [])

    url: str = Field(default = None)
    base_url: str = Field(default = None)
    relative_url: str = Field(default = None)

    _unserializable = ['_downloader', '_page', '_page_response']

    async def _init_hook(self):
        if self._crawler:
            await self._crawler.register(self)
        else:
            self.log('crawler not passed')

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

    def get_page_links(self):
        for page in self.page_links:
            if page != None:
                yield page

    async def from_url(self, url: str):
        # gymnastics
        self._page = await self._downloader.webdriver.new_page(self._crawler)
        await self._init_hook()

        self.log('going to {0}'.format(url))

        self._page_response = await self._page.goto(url)

    async def from_html(self, url: str, html: str):
        self._page = await self._downloader.webdriver.new_page(self._crawler)
        await self._init_hook()

        async def handle_route(route, request):
            await route.fulfill(
                status=200,
                content_type="text/html",
                body=html
            )

        await self._page.get().route(url, handle_route)

        #self._page.url_override = url

        self._page_response = await self._page.goto(url)
        #await self._page.get().evaluate("() => {document.write(`"+html+"`);}")

    async def set_info(self):
        self.set_title(await self._page.get_title())
        self.url = self._page.get_url(True)
        self.base_url = self._page.get_base_url()
        self.relative_url = await self._page.get_relative_url()

    async def get_encoding(self):
        page = self._page.get()
        #charset = await page.locator('meta[charset]').get_attribute('charset')
        #if charset:
        #    return charset

        #content_type = await page.locator('meta[http-equiv=\"Content-Type\"]').get_attribute('content')
        #if content_type and 'charset=' in content_type:
        #    return content_type.split('charset=')[1].lower()

        try:
            content_type = self._page_response.headers.get('content-type', '')
            if 'charset=' in content_type.lower():
                return content_type.lower().split('charset=')[1].split(';')[0].strip()
            elif 'utf-8' in content_type.lower():
                return 'utf-8'
        except Exception as e:
            self.log_error(e)

        return 'utf-8'

    # crawling methods

    def set_downloader(self, downloader):
        self._downloader = downloader

    def set_crawler(self, crawler):
        self._crawler = crawler(ref = self)

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

    @classmethod
    def _creations(cls) -> list:
        return [
            CreationItem(
                name = 'Web page',
                object_name = 'Web.Pages.Page',
                create = 'Web.Pages.Get'
            )
        ]
