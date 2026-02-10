from App.Objects.Object import Object
from Web.DownloadManager.Item import Item as DownloadManagerItem
from Web.HTTP.Headers import Headers
from pydantic import Field
from typing import Type
from App.Data.Increment import Increment
import asyncio#, aiohttp

class Manager(Object):
    class DownloadManagerItems(Object):
        items: list = None
        downloads: Type[Increment] = None

        def constructor(self):
            self.items = []
            self.downloads = Increment()

        def append(self, item: DownloadManagerItem):
            self.items.append(item)

        def remove(self, item: DownloadManagerItem):
            pass

        def getById(self, id: int):
            for item in self.items:
                if item.id == id:
                    return item

    max_concurrent_downloads: int = Field(default = 3)
    max_kbps_speed: int = Field(default = None)
    timeout_seconds: int = Field(default = 10)
    queue: DownloadManagerItems = None

    semaphore: Type[asyncio.Semaphore] = None
    #timeout: Type[aiohttp.ClientTimeout] = None
    #session: Type[aiohttp.ClientSession] = None
    queue: DownloadManagerItems = None

    def constructor(self):
        self.max_concurrent_downloads = self.getOption('download_manager.max_concurrent_downloads')
        self.max_kbps_speed = self.getOption('download_manager.max_kbps_speed')
        self.timeout_seconds = self.getOption("download_manager.timeout_seconds")
        self.queue = self.DownloadManagerItems()

    @classmethod
    def mount(cls):
        from App import app

        manager = cls()

        app.mount('DownloadManager', manager)

    def getHeaders(self) -> dict:
        _headers = Headers()
        _headers.user_agent = self.getOption("download_manager.user_agent")

        return _headers.model_dump(by_alias = True)

    @classmethod
    def getSettings(cls):
        from App.Arguments.Types.Int import Int

        return [
            Int(
                name = "download_manager.max_concurrent_downloads",
                default = 3,
            ),
            Int(
                name = "download_manager.max_kbps_speed",
                default = 2000,
            ),
            Int(
                name = "download_manager.timeout_seconds",
                default = 100
            ),
            Int(
                name = "download_manager.user_agent",
                default = ""
            ),
        ]
