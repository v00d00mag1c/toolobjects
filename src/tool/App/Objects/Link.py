from App.Objects.Object import Object
from typing import Any, Literal
from pydantic import Field
from enum import Enum

class LinkTypeEnum(Enum):
    CONTENT = 0 # will be used for json content insertion
    EXTERNAL = 1

class Link(Object):
    '''
    Link to an object
    '''

    item: Object = Field()
    common: bool = Field(default = False)
    thumbnail: bool = Field(default = False)
    revision: bool = Field(default = False)
    link_type: LinkTypeEnum = Field(default = LinkTypeEnum.CONTENT.value)
