from App.Objects.Act import Act
from App.Objects.Arguments.Argument import Argument
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.AllowedValues import AllowedValues
from Web.Crawler.Webdrivers.Chromedriver.Chromedriver import Chromedriver
from Web.Crawler.Webdrivers.Chromedriver.Add import Add
from Data.Types.String import String
from App import app
from pathlib import Path
import aiohttp

class Download(Act):
    @classmethod
    def _arguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
            Argument(
                name = 'channel',
                allowed_values = AllowedValues(
                    values = ['Stable', 'Beta', 'Canary', 'Dev'],
                    strict = True,
                ),
                orig = String,
                default = 'Stable'
            )
        ])

    async def _implementation(self, i):
        _bin = app.Storage.get('bin')

        channels = await self._get_versions()
        channel = channels.get(i.get('channel'))

        item = Chromedriver()
        item.platform = Chromedriver._get_platform()
        item.version = i.get('version')
        item.revision = i.get('revision')

        downloads = channel.get('downloads')
        # chrome = downloads.get('chrome')

        driver_item = None
        shell_item = None

        for _item in downloads.get('chromedriver'):
            if _item.get('platform') == item.platform:
                driver_item = _item

        for _item in downloads.get('chrome-headless-shell'):
            if _item.get('platform') == item.platform:
                shell_item = _item

        assert driver_item != None
        assert shell_item != None

        unit = _bin.storage_adapter.get_storage_unit()
        root: Path = unit.get_root()

        for item in [{
            'item': driver_item,
            'type': 'chromedriver',
            'name': 'driver.zip'
        },{
            'item': shell_item,
            'type': 'shell',
            'name': 'shell.zip'
        }]:
            _item = app.DownloadManager.addURL(item.get('item').get('url'), str(root), item.get('name'))
            await _item.start()

            self.log_success('{0} is downloaded'.format(item.get('type')))

        _add = Add()
        _res = await _add.execute({
            'driver': item,
            'storage_unit': unit,
            'driver_zip': str(root.joinpath('driver.zip')),
            'shell_zip': str(root.joinpath('shell.zip'))
        })

        root.joinpath('driver.zip').unlink()
        root.joinpath('shell.zip').unlink()

        return _res

    async def _get_versions(self):
        version = "https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json"

        async with aiohttp.ClientSession() as session:
            async with session.get(version) as response:
                channels = await response.json()

        channel = channels.get('channels')

        return channel
