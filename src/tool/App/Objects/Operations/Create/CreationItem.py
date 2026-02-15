from App.Objects.Object import Object
from pydantic import Field

class CreationItem(Object):
    name: str = Field(default = None)
    object_name: str = Field(default = None)
    create: str = Field(default = None)
    key_is_name: bool = Field(default = False)
