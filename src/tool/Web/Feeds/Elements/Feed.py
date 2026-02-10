from App.Objects.Object import Object
from Web.Feeds.Protocols.RSS import RSS
from Web.Feeds.Protocols.Atom import Atom
import xml.etree.ElementTree as ET

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
        _type = data.tag.split('}', 1)
        if len(_type) < 2:
            _type = _type[0]
        else:
            _type = _type[1]

        if _type == 'feed':
            return Atom
        elif _type == 'rss' or _type == 'RDF':
            return RSS
