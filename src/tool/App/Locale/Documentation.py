from App.Objects.Mixins.BaseModel import BaseModel
from App.Locale.Key import Key
from pydantic import Field

class Documentation(BaseModel):
    '''
    Description of something on english text
    '''

    name: Key = Field(default = None)
    description: Key = Field(default = None)

    def get_name(self):
        if self.name:
            return self.name.value

    def get_description(self):
        if self.description:
            return self.description.value
