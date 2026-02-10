from App.Objects.Object import Object
from pydantic import Field

class ChannelImage(Object):
    url: str = Field(default = None)
    title: str = Field(default = None)
    channel_link: str = Field(default = None, alias = 'link')
