from ..Argument import Argument
from pydantic import Field
from App import app

class Executable(Argument):
    str_type: str = Field(default = None)

    def implementation(self, original_value: str):
        return app.objects.getByName(key = original_value)

    @property
    def none_message(self):
        return 'not found'
