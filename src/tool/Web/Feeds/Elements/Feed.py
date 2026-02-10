from App.Objects.Object import Object
from Web.Feeds.Protocols.RSS import RSS
from Web.Feeds.Protocols.Atom import Atom
import xml.etree.ElementTree as ET
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Argument import Argument
from Data.Types.Boolean import Boolean

class Feed(Object):
    @classmethod
    async def download(cls, url: str) -> str:
        import aiohttp

        response_xml = None
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response_xml = await response.text()

        return response_xml

    @classmethod
    def detect_type(cls, data: ET):
        if data.find('rss'):
            return RSS

        if data.find('feed'):
            return Atom

    @classmethod
    def getArguments(cls):
        return ArgumentDict(items = [
            Argument(
                name = 'download.thumbnails',
                orig = Boolean,
                default = True
            )
        ])
