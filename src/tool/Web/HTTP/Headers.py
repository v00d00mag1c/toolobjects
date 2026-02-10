from App.Objects.Object import Object
from pydantic import Field

class Headers(Object):
    user_agent: str = Field(default=None, alias="User-Agent")
    accept: str = Field(default = None, alias = 'Accept')
    accept_language: str = Field(default = None, alias = 'Accept-Language')
    accept_encoding: str = Field(default = None, alias = 'Accept-Encoding')
    accept_ranges: str = Field(default = None, alias = 'Accept-Ranges')
    cache_control: str = Field(default = None, alias = 'Cache-Control')
