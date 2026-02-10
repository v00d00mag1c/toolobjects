from App.Objects.Object import Object
from pydantic import Field

class URL(Object):
    value: str = Field()
