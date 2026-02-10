from App.Objects.Mixins.BaseModel import BaseModel
from pydantic import Field

class Thumbnail(BaseModel):
    obj: BaseModel = Field()
