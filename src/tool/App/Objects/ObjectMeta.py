from pydantic import BaseModel, Field

class ObjectMeta(BaseModel):
    '''
    Additional data about object
    '''
    name: str = Field(default=None)
    description: str = Field(default=None)
    indexation: str = Field(default=None)
    original_name: str = Field(default=None)
    original_description: str = Field(default=None)
    thumbnail: dict = Field(default = None)
    duration: int = Field(default = None)
