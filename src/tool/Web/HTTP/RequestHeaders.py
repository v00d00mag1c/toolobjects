from App.Objects.Object import Object
from pydantic import Field

class RequestHeaders(Object):
    user_agent: str = Field(default=None, alias="user-agent")
    accept: str = Field(default = None, alias = 'accept')
    accept_language: str = Field(default = None, alias = 'accept-language')
    accept_encoding: str = Field(default = None, alias = 'accept-encoding')
    accept_ranges: str = Field(default = None, alias = 'accept-ranges')
    cache_control: str = Field(default = None, alias = 'cache-control')
    content_type: str = Field(default = None, alias = 'content-type')
