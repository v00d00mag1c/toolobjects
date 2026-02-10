from App.Objects.Object import Object
from Web.Feeds.Elements.Element import Element
from pydantic import Field
from typing import Optional
from datetime import datetime
import xml.etree.ElementTree as ET

class Channel(Element):
    url: Optional[str] = Field(default = None)
    channel_index: Optional[int] = Field(default = 0)
    channel_link: Optional[str] = Field(default = None)
    generator: Optional[str] = Field(default = None)
    copyright: Optional[str] = Field(default = None)
    ttl: Optional[str] = Field(default = None)
    last_build_date: datetime = Field(default = None)
    langs: Optional[list[str]] = Field(default = [])

    def get_original_url(self):
        return self.obj.source[0].obj.get('value')
