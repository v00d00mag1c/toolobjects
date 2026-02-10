from App.Objects.Mixins.BaseModel import BaseModel
from pydantic import Field
from typing import Literal

class ItemPermission(BaseModel):
    uuid: int = Field()
    user: str = Field()
    action: Literal['view', 'delete', 'edit', 'link'] = Field()
    allow: bool = Field(default = True)
