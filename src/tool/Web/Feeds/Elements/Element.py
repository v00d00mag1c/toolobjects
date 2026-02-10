from App.Objects.Object import Object
from pydantic import Field
from typing import Optional
from Web.Feeds.Elements.Link import Link
from Web.Feeds.Elements.Author import Author
import xml.etree.ElementTree as ET

class Element(Object):
    id: Optional[str] = Field(default = None)
    guid: Optional[str] = Field(default = None)
    title: Optional[str] = Field(default = None)
    subtitle: Optional[str] = Field(default = None)
    description: Optional[str] = Field(default = None)
    link_items: Optional[list[Link]] = Field(default = [])
    language: Optional[str] = Field(default = None)
    author: list[Author] = Field(default = [])
