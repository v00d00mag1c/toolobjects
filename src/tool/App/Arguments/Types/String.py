from ..Argument import Argument

class String(Argument):
    def implementation(self, original_value: str):
        if original_value == None:
            return None

        return str(original_value)
