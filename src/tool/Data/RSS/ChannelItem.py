from App.Objects.Object import Object
from pydantic import Field
import datetime
from typing import Optional
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime

class ChannelItem(Object):
    title: str = Field(default = None)
    description: str = Field(default = None)
    channel_link: str = Field(default = None, alias = 'link')
    guid: Optional[dict | str] = Field(default = None)
    pubDate: datetime.datetime = Field(default = None)
    media_thumbnail: Optional[dict] = Field(alias="media:thumbnail", default = None)

    @classmethod
    def fromElement(cls, xml: ET):
        element = cls()

        if xml.find('title') != None:
            element.title = xml.find('title').text

        if xml.find('description') != None:
            element.description = xml.find('description').text

        if xml.find('link') != None:
            element.channel_link = xml.find('link').text

        if xml.find('guid') != None:
            element.guid = xml.find('guid').text

        if xml.find('media:thumbnail') != None:
            element.media_thumbnail = xml.find('media:thumbnail').text

        if xml.find('pubDate') != None:
            element.pubDate = parsedate_to_datetime(xml.find('pubDate').text)

        return element
