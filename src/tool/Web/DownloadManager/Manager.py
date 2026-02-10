from App.Objects.Object import Object
from App.Objects.Misc.Increment import Increment
from App.Objects.Arguments.Argument import Argument
from Web.DownloadManager.Item import Item
from App.Storage.StorageUnit import StorageUnit
from Web.HTTP.RequestHeaders import RequestHeaders
from Data.Types.Int import Int
from Data.Types.Boolean import Boolean
from Data.Types.String import String
from pydantic import Field
from typing import Any
import asyncio#, aiohttp
from Web.HTTP.UserAgent import UserAgent

class Manager(Object):
    class DownloadManagerItems(Object):
        items: list = None
        downloads: Any = None

        def init_hook(self):
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
    semaphore: Any = None
    timeout: Any = None
    session: Any = None

    def addURL(self, url: str, dir: StorageUnit | str = None, name: str = None) -> Item:
        self._check()

        _dir = ''
        if dir != None:
            _dir = dir
        if isinstance(_dir, StorageUnit):
            if name == None:
                name = _dir.hash + '.oct'
            _dir.setCommonFile(_dir.getDir().joinpath(name))
            _dir = str(_dir.getDir())
        else:
            _dir = str(_dir)

        _item = Item(
            url = url,
            download_dir = _dir,
            name = name
        )
        _item._manager_link = self
        _item._init_hook()

        self.queue.append(_item)

        return _item

    def _check(self):
        if self.session == None:
            self._init_hook()

    def getSession(self):
        import aiohttp

        if self.timeout == None:
            self.timeout = aiohttp.ClientTimeout(total = self.getOption("download_manager.timeout_seconds"))

        return aiohttp.ClientSession(timeout = self.timeout)

    def _init_hook(self):
        '''
        bc it loads before loop creates
        '''
        self.session = self.getSession()

    @classmethod
    def mount(cls):
        from App import app

        manager = cls()
        manager.queue = cls.DownloadManagerItems(
            max_kbps_speed = cls.getOption('download_manager.max_concurrent_downloads')
        )
        manager.semaphore = asyncio.Semaphore(manager.queue.max_kbps_speed)

        app.mount('DownloadManager', manager)

    def getHeaders(self) -> dict:
        _headers = RequestHeaders()
        _headers.user_agent = UserAgent.get_or_generate()
        _headers.accept = self.getOption('download_manager.headers.accept')
        _headers.accept_encoding = self.getOption('download_manager.headers.accept-encoding')
        _headers.accept_language = self.getOption('download_manager.headers.accept-language')

        return _headers

    @classmethod
    def _settings(cls):
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
                name = "download_manager.total_timeout",
                default = 0,
                orig = Int
            ),
            Argument(
                name = "download_manager.timeout",
                default = 100,
                orig = Int
            ),
            Argument(
                name = "download_manager.headers.user-agent", # pass '' to randomize
                default = 'toolobjects/0.1',
                orig = String
            ),
            Argument(
                name = "download_manager.headers.accept-encoding",
                #default = 'gzip, deflate, br, zstd',
                default = '',
                orig = String
            ),
            Argument(
                name = "download_manager.headers.accept-language",
                default = 'en_US',
                orig = String
            ),
            Argument(
                name = "download_manager.headers.accept",
                default = 'text/html,application/xhtml+xml,application/xml,image/avif,image/webp,image/apng,*/*',
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
