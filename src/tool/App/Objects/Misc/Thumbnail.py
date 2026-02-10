from App.Objects.Mixins.BaseModel import BaseModel
from pydantic import Field
from typing import Literal, Optional

class Thumbnail(BaseModel):
    role: Optional[list[Literal['image', 'video']]] = Field(default = None)
    obj: BaseModel = Field()
