from Web.Feeds.Protocols.FeedProtocol import FeedProtocol
from Web.Feeds.Elements.Channel import Channel
from Web.Feeds.Elements.Author import Author
from Web.Feeds.Elements.Entry import Entry
from Web.Feeds.Elements.EntryContent import EntryContent
from Web.Feeds.Elements.Link import Link
from App.Objects.Object import Object
from email.utils import parsedate_to_datetime
import xml.etree.ElementTree as ET
from typing import Generator

class RSS(FeedProtocol):
    def _get_channels(self, data: ET):
        _items = list()
        for channel in data.find('.//channel'):
            _channel = Channel()
            _items.append(_channel)

            for key in ['title', 'ttl', 'description', 'link', 'lastBuildDate', 'language', '{dc}:creator']:
                _val = data.find('.//'+key)

                match(key):
                    case 'title':
                        _channel.obj.name = _val.text
                    case 'link':
                        _channel.link_items.append(self._get_link(_val))
                    case 'lastBuildDate':
                        _channel.last_build_date = self._date_to_str(_val.text)
                    case 'dc:creator':
                        _channel.author.append(Author(
                            name = _val
                        ))
                    case _:
                        if _val != None:
                            setattr(_channel, key, _val.text)

        return _items[0]

    def _get_link(self, data):
        _self = Link()
        _self.value = data.get('href')

        return _self

    def _get_entries(self, channel: Channel, data: ET) -> Generator[Entry]:
        for entry in data.findall('.//item'):
            yield self._get_entry(entry)

    def _date_to_str(self, val: str):
        return parsedate_to_datetime(val)

    def _get_entry(self, data: ET):
        entry = Entry()

        for key in ['title', 'summary', 'description', 'link', 'pubDate']:
            _val = data.find('./'+key)

            match(key):
                case 'title':
                    entry.obj.name = _val.text
                case 'description':
                    entry.content = EntryContent(
                        type = _val.get('type'),
                        content = _val.text,
                    )
                case 'pubDate':
                    if _val != None:
                        entry.obj.created_at = self._date_to_str(_val.text)
                case _:
                    setattr(entry, key, _val)

        for link in data.find('./link'):
            entry.link_items.append(self._get_link(link))

        return entry
