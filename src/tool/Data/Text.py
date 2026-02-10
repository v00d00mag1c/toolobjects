from App.Objects.Object import Object
from App.Objects.LinkInsertion import LinkInsertion
from pydantic import Field

class Text(Object):
    text: str | LinkInsertion = Field(default = '')
