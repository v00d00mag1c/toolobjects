from ...Arguments.Argument import Argument

class Int(Argument):
    def implementation(self, original_value: str):
        if original_value == None:
            return None

        return int(original_value)
