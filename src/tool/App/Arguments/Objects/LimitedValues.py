from ...Arguments.Argument import Argument
from pydantic import Field, computed_field
from App import app

# its like <select> in html or radioboxes idk
class LimitedValues(Argument):
    values: list[Argument] = Field(default = [])
    strict: bool = Field(default = True)

    def implementation(self, original_value: str):
        is_in = False

        if self.strict == True:
            for value in self.values:
                if original_value == value.name:
                    is_in = True
        else:
            is_in = True

        assert is_in == True, "not allowed value"

        return original_value
