from pydantic import BaseModel, Field

class ObjectMeta(BaseModel):
    '''
    Additional data about object
    '''
    thumbnail: dict = Field(default = None)
    duration: int = Field(default = None)
