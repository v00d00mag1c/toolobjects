from pydantic import Field
from App.Objects.Mixins.BaseModel import BaseModel

class SavedVia(BaseModel):
    object_name: str = Field(default = None)
    executable_name: str = Field(default = None)
    call_id: int = Field(default = None)
