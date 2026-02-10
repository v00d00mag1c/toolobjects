from pydantic import Field
from typing import Optional
from App.Objects.Mixins.BaseModel import BaseModel

class Source(BaseModel):
    '''
    Where from an object was obtained
    '''
    types: Optional[str] = Field(default = None)
    content: Optional[str] = Field(default = None)
