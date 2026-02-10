from App.Objects.Mixins.BaseModel import BaseModel
from App.Locale.Key import Key
from pydantic import Field

class Documentation(BaseModel):
    '''
    Description of something on english text
    '''

    name: Key = Field(default = None)
    description: Key = Field(default = None)
