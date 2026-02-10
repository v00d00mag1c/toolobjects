from Web.Crawler.Webdrivers.Webdriver import Webdriver
from pydantic import Field
from typing import Any
import platform
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService

class Chromedriver(Webdriver):
    version: str = Field(default = None)
    revision: str | int = Field(default = None)
    _driver: Any = None
    #_service: Any = None

    async def start(self):
        log_path = 'NUL'

        _options = webdriver.ChromeOptions()
        _options.binary_location = str(self.get_shell())
        _options.add_argument('--start-maximized')
        _options.add_argument('--start-fullscreen')
        _options.add_argument('--headless')
        _options.add_argument('--no-sandbox')
        _options.add_argument('--window-size=1920,1200')
        _options.add_argument('--user-agent={0}'.format(self.get_useragent()))

        service = ChromeService(executable_path = self.get_webdriver(),
                                chrome_options = _options,
                                log_path = log_path)

        self._driver = webdriver.Chrome(service=service, options=_options)

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
