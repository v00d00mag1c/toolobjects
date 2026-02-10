from App.Objects.Object import Object
from App.Objects.Misc.LinkInsertion import LinkInsertion
from pydantic import Field

class Text(Object):
    value: str | LinkInsertion = Field(default = '')
