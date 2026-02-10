from Web.Feeds.Protocols.FeedProtocol import FeedProtocol
from Web.Feeds.Elements.Channel import Channel
from Web.Feeds.Elements.Link import Link
from Web.Feeds.Elements.Entry import Entry
import xml.etree.ElementTree as ET
from typing import ClassVar

class Atom(FeedProtocol):
    protocol_name = 'atom'
    namespaces: ClassVar[dict] = {
        'xmlns':"http://www.w3.org/2005/Atom"
    }

    async def parse(self, data: ET):
        _channel = self._get_channel(data)

        for entry in data.findall('./xmlns:entry', self.namespaces):
            _entry = self._get_entry(entry)
            _channel.link(_entry)

        return [_channel]

    def _get_channel(self, data: ET):
        channel = Channel()

        for key in ['title', 'subtitle', 'id', 'link']:
            _val = data.find('./xmlns:'+key, self.namespaces)

            match(key):
                case 'title':
                    channel.obj.name = _val.text
                case 'link':
                    channel.link_item = Link.from_xml(data.find('link'))
                case _:
                    if _val != None:
                        setattr(channel, key, _val.text)

        return channel

    def _get_entry(self, data: ET):
        entry = Entry()

        return entry
