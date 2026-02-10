from Web.Pages.Crawler.Webdrivers.Webdriver import Webdriver
from Web.Pages.Crawler.Webdrivers.WebdriverPage import WebdriverPage
from pydantic import Field
from typing import Any
import platform
from playwright.async_api import Playwright, async_playwright

class Chromedriver(Webdriver):
    version: str = Field(default = None)
    revision: str | int = Field(default = None)
    viewport: dict = Field(default = {})
    executable_path: str = Field(default = None)

    _playwright: Any = None
    _browser: Any = None
    _context: Any = None
    #_service: Any = None

    async def start(self, i):
        size = i.get('webdriver.sizes').split(',')

        self._playwright = await async_playwright().start()

        self.log('launching browser')

        self._browser = await self._launch_browser(i)

        self._context = await self._browser.new_context(
            viewport = None,
            user_agent = self.get_useragent(),
        )

        self.viewport = {"width": int(size[0]), "height": int(size[1])}

    async def _launch_browser(self, i):
        args = [
            '--start-maximized',
            '--start-fullscreen',
            '--headless',
            '--no-sandbox',
            '--user-agent={0}'.format(self.get_useragent())
        ]
        for argument in i.get('webdriver.args'):
            args.append(argument)

        executable_path = self.executable_path
        if executable_path == None:
            executable_path = str(self.get_shell())

        return await self._playwright.chromium.launch(
            executable_path = executable_path,
            args = args,
            headless = i.get('webdriver.headless')
        )

    async def new_page(self):
        page = WebdriverPage()
        page._page = await self._context.new_page()
        await page.setViewport(self.viewport)

        return page

    def clear(self):
        self._context.close()
        self._browser.close()
        self._playwright.stop()

    def get_shell(self):
        return self._get('file').get_root().joinpath('chrome').joinpath('chrome-headless-shell.exe')

    def get_webdriver(self):
        return self._get('file').get_root().joinpath('driver').joinpath('chromedriver.exe')

    @staticmethod
    def _get_platform():
        version = ['', '']
        system_type = platform.system().lower()
        architecture = platform.machine().lower() 

        if architecture in ['x86_64', 'amd64']:
            version[1] = '64'
        elif architecture in ['i386', 'i686', 'x86']:
            version[1] = '32'
        elif architecture in ['arm64', 'aarch64']:
            version[1] = 'arm64'
        else:
            version[1] = architecture

        match system_type:
            case "darwin":
                if architecture in ['arm64', 'aarch64']:
                    version[1] = "arm64"
                else:
                    version[1] = "x64"

                version[0] = 'mac-'
            case "windows":
                version[0] = 'win'
            case _:
                version[0] = 'win'

        return ''.join(version)
