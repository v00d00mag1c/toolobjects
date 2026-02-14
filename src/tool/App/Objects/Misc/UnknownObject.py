from App.Objects.Object import Object
from pydantic import Field

class UnknownObject(Object):
    '''
    returns if object with specified name was not found
    '''

    reason: str = Field(default = None)
    original_content: dict = Field(default = {})

    def to_db_json(self):
        return self.original_content
