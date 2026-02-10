from App.Objects.Mixins.BaseModel import BaseModel
from pydantic import Field
from typing import Literal, Optional

class ObjectPermission(BaseModel):
    object_name: str = Field()
    user: Optional[str] = Field() # Allow without log?
    action: Literal['call', 'view'] = Field(default = 'call')
    allow: bool = Field(default = True)
