from App.Objects.Object import Object
from pydantic import Field
from typing import Optional

class Element(Object):
    id: Optional[str] = Field(default = None)
    title: Optional[str] = Field(default = None)
    subtitle: Optional[str] = Field(default = None)
    description: Optional[str] = Field(default = None)
