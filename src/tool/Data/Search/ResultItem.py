from App.Objects.Object import Object
from pydantic import Field

class ResultItem(Object):
    icon: str = Field(default = None)
    title: str = Field(default = None)
    description: str = Field(default = '')
    url: str = Field(default = None)
