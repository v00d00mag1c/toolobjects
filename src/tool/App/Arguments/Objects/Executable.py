from ..Argument import Argument
from pydantic import Field
from App import app

class Executable(Argument):
    str_type: str = Field(default = None)

    def implementation(self, original_value: str):
        obj = app.app.objects.getByName(key = original_value)
        if obj == None:
            return None

        return obj.getModule()

    @property
    def none_message(self):
        return 'not found'
