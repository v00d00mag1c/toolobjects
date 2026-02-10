from App.Objects.Mixins.BaseModel import BaseModel
from pydantic import Field

class Key(BaseModel):
    '''
    Description of something
    '''

    value: str = Field(default = '')
    id: str = Field(default = '')

    def get_value(self, values: list = []) -> str:
        return self.value.format(*values)
