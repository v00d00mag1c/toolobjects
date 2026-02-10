from Web.Feeds.Protocols.FeedProtocol import FeedProtocol
from Web.Feeds.Elements.Channel import Channel
from Web.Feeds.Elements.Author import Author
from Web.Feeds.Elements.Entry import Entry
from Web.Feeds.Elements.EntryContent import EntryContent
from Web.Feeds.Elements.Link import Link
from Media.Images.Image import Image
from App.Objects.Misc.Increment import Increment
from email.utils import parsedate_to_datetime
import xml.etree.ElementTree as ET
from typing import AsyncGenerator
from typing import ClassVar, Generator

class RSS(FeedProtocol):
    namespaces: ClassVar[dict] = {
        'media': ""
    }

    def _get_channels(self, data: ET):
        items = list()

        i = Increment()

        for channel in data.find_all('channel'):
            new_channel = Channel()
            new_channel.channel_index = i.getIndex()
            items.append(new_channel)

            for item in channel.find_all('title', recursive=False):
                new_channel.obj.name = item.get_text()

            for item in channel.find_all('ttl', recursive=False):
                new_channel.ttl = item.get_text()

            for item in channel.find_all('link', recursive=False):
                link = Link()
                link.value = item.get_text()

                new_channel.link_items.append(link)

            for item in channel.find_all('lastBuildDate', recursive=False):
                new_channel.last_build_date = self._date_to_str(item.get_text())

            for item in channel.find_all('language', recursive=False):
                new_channel.langs.append(item.get_text())

            for item in channel.find_all('dc:creator', recursive=False):
                new_channel.author.append(Author(
                    name = item.get_text()
                ))

        return items

    async def _get_entries(self, channel: Channel, data: ET, i: dict) -> AsyncGenerator[Entry]:
        for entry in data.find_all('item'):
            yield await self._get_entry(entry, i)

    def _date_to_str(self, val: str):
        return parsedate_to_datetime(val)

    async def _get_entry(self, data: ET, i: dict):
        entry = Entry()

        for item in data.find_all('title', recursive=False):
            entry.obj.name = item.text

        self.log('entry: '+entry.obj.name)

        for item in data.find_all('summary', recursive=False):
            entry.summary = item.text

        for item in data.find_all('description', recursive=False):
            entry.content = EntryContent(
                type = item.get('type'),
                content = item.text,
            )
            await entry.content.update()

        for item in data.find_all('link', recursive=False):
            link = Link()
            link.value = item.text

            entry.link_items.append(link)

        for item in data.find_all('pubDate', recursive=False):
            if item != None:
                entry.obj.created_at = self._date_to_str(item.text)

        for item in data.find_all('media:thumbnail', recursive=False):
            if i.get('download.thumbnails'):
                try:
                    _img = await Image.from_url(item.get('url'))
                    entry.link(_img, role = ['thumbnail'])

                    self.log('entry {0}: media:thumbnail {1}'.format(entry.obj.name, item.get('url')))
                except Exception as e:
                    self.log_error(e, exception_prefix = "entry {0}: media:thumbnail download error. ".format(entry.obj.name))

        return entry
