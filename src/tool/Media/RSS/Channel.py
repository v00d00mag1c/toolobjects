from App.Objects.Object import Object
from Media.RSS.ChannelImage import ChannelImage
from Media.RSS.ChannelItem import ChannelItem
from pydantic import Field
from typing import Optional
import xml
import xml.etree.ElementTree as ET

class Channel(Object):
    title: str = Field(default = None)
    description: str = Field(default = None)
    url: str | None = Field(default = None)
    channel_link: str = Field(default = None, alias='link')
    generator: str | None = Field(default = None)
    copyright: str | None = Field(default = None)
    language: str | None = Field(default = None)
    ttl: int | None = Field(default = None)
    image: Optional[ChannelImage] = Field(default = None)

    def update_data(self, channel: dict):
        self.title = channel.get('title')
        self.description = channel.get('description')
        self.channel_link = channel.get('link')
        self.generator = channel.get('generator')
        self.copyright = channel.get('copyright')
        self.language = channel.get('language')

    @classmethod
    def fromElement(cls, element: ET):
        channel = cls()
        for key in ['title', 'description', 'link', 'generator', 'copyright', 'language']:
            if element.find(key) != None:
                setattr(channel, key, element.find(key).text)

        return channel
