from pydantic import BaseModel, Field

class Saved(BaseModel):
    name: str = Field(default = None)
    method: str = Field(default = None)
    call: int = Field(default = None)
