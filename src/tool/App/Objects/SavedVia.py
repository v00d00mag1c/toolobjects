from pydantic import BaseModel, Field

class SavedVia(BaseModel):
    object_name: str = Field(default = None)
    custom_object_name: str = Field(default = None)
    executable_name: str = Field(default = None)
    call_id: int = Field(default = None)
