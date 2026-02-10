from App.Objects.Object import Object
from App.Objects.Misc.Increment import Increment
from App.Objects.Arguments.Argument import Argument
from Web.DownloadManager.Item import Item
from App.Storage.StorageUnit import StorageUnit
from Web.HTTP.Headers import Headers
from Data.Int import Int
from Data.Boolean import Boolean
from Data.String import String
from pydantic import Field
from typing import Type
import asyncio#, aiohttp

class Manager(Object):
    class DownloadManagerItems(Object):
        items: list = None
        downloads: Type[Increment] = None

        def constructor(self):
            self.items = []
            self.downloads = Increment()

        def append(self, item: Item):
            self.items.append(item)

        def remove(self, item: Item):
            self.items.remove(item)

        def getById(self, id: int):
            for item in self.items:
                if item.id == id:
                    return item

    max_kbps_speed: int = None
    queue: DownloadManagerItems = None
    semaphore: Type[asyncio.Semaphore] = None
    #timeout: Type[aiohttp.ClientTimeout] = None
    session: Type = None

    def addURL(self, url: str, dir: StorageUnit | str = None, name: str = None) -> Item:
        self._check()

        _dir = ''
        if dir != None:
            _dir = dir
        if isinstance(_dir, StorageUnit):
            _dir = str(_dir.getDir())
            if name == None:
                name = _dir.hash + '.oct'

        _item = Item(
            url = url,
            download_dir = _dir,
            name = name
        )
        _item._manager_link = self
        _item._constructor()

        self.queue.append(_item)

        return _item

    def _check(self):
        if self.session == None:
            self._constructor()

    def _constructor(self):
        '''
        bc it loads before loop creates
        '''
        import aiohttp

        self.session = aiohttp.ClientSession(
            timeout = self.timeout,
        )

    @classmethod
    def mount(cls):
        from App import app
        import aiohttp

        manager = cls()
        manager.queue = cls.DownloadManagerItems(
            max_kbps_speed = cls.getOption('download_manager.max_concurrent_downloads')
        )
        manager.semaphore = asyncio.Semaphore(manager.queue.max_kbps_speed)
        manager.timeout = aiohttp.ClientTimeout(total = cls.getOption("download_manager.timeout_seconds"))

        app.mount('DownloadManager', manager)

    def getHeaders(self) -> dict:
        _headers = Headers()
        _headers.user_agent = self.getOption("download_manager.user_agent")

        return _headers.to_json(by_alias = True)

    @classmethod
    def getSettings(cls):
        return [
            Argument(
                name = "download_manager.max_concurrent_downloads",
                default = 3,
                orig = Int
            ),
            Argument(
                name = "download_manager.max_kbps_speed",
                default = 2000,
                orig = Int
            ),
            Argument(
                name = "download_manager.timeout_seconds",
                default = 100,
                orig = Int
            ),
            Argument(
                name = "download_manager.user_agent",
                default = "",
                orig = String
            ),
            Argument(
                name = 'download_manager.new_session_per_download',
                default = False,
                orig = Boolean
            ),
            Argument(
                name = 'download_manager.allow_redirects',
                default = True,
                orig = Boolean
            )
        ]

    @classmethod
    def getClassEventTypes(cls) -> list:
        return ['downloading', 'success', 'ended', 'started']
