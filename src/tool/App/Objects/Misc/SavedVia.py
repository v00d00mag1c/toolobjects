from pydantic import Field
from App.Objects.Mixins.BaseModel import BaseModel
from typing import Optional

class SavedVia(BaseModel):
    object_name: Optional[str] = Field(default = None)
    executable_name: Optional[str] = Field(default = None)
    # call_id: Optional[int] = Field(default = None)
