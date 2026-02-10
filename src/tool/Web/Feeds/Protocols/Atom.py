from Web.Feeds.Protocols.FeedProtocol import FeedProtocol
from Web.Feeds.Elements.Channel import Channel
from Web.Feeds.Elements.Link import Link
from Web.Feeds.Elements.Entry import Entry
from Web.Feeds.Elements.EntryContent import EntryContent
import xml.etree.ElementTree as ET
from typing import ClassVar, Generator
from email.utils import parsedate_to_datetime
from datetime import datetime

class Atom(FeedProtocol):
    protocol_name = 'atom'
    namespaces: ClassVar[dict] = {
        'xmlns':"http://www.w3.org/2005/Atom"
    }

    def _get_entries(self, channel: Channel, data: ET) -> Generator[Entry]:
        for entry in data.findall('./xmlns:entry', self.namespaces):
            yield self._get_entry(entry)

    def _get_channels(self, data: ET):
        channel = Channel()
        for key in ['title', 'subtitle', 'id', 'link']:
            _val = data.find('./xmlns:'+key, self.namespaces)

            match(key):
                case 'title':
                    channel.obj.name = _val.text
                case 'link':
                    channel.link_items.append(self._get_link(_val))
                case _:
                    if _val != None:
                        setattr(channel, key, _val.text)

        return [channel]

    def _get_link(self, data):
        _self = Link()
        for key in ['href', 'rel', 'type', 'hreflang', 'title', 'length']:
            set_key = key
            if key == 'href':
                set_key = 'value'

            setattr(_self, set_key, data.get(key))

        return _self

    def _date_to_str(self, val: str):
        for fmt in [
            "%Y-%m-%dT%H:%M:%SZ",
            "%Y-%m-%dT%H:%M:%S%z",
            "%Y-%m-%dT%H:%M:%S",
        ]:
            try:
                return datetime.strptime(val, fmt)
            except ValueError:
                continue

    def _get_entry(self, data: ET):
        _title = data.find('./xmlns:title', self.namespaces)
        _summary = data.find('./xmlns:summary', self.namespaces)
        _content = data.find('./xmlns:content', self.namespaces)

        entry = Entry()

        if _title != None:
            entry.obj.name = _title.text
        if _summary != None:
            entry.summary = _summary.text
        if _content != None:
            entry.content = EntryContent(
                type = _content.get('type'),
                content = _content.text,
            )

        for link in data.find('./xmlns:link', self.namespaces):
            entry.link_items.append(self._get_link(link))

        _published = data.find('./xmlns:published', self.namespaces)
        _edited = data.find('./xmlns:updated', self.namespaces)
        if _published != None:
            entry.obj.created_at = self._date_to_str(_published.text)
        else:
            if _edited != None:
                entry.obj.created_at = self._date_to_str(_edited.text)

        if _edited != None:
            entry.obj.updated_at = self._date_to_str(_edited.text)

        return entry
