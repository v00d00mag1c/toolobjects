from App.Objects.Object import Object
from pydantic import Field

class Bookmark(Object):
    url: str = Field(default = None)
