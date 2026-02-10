from ...Arguments.Argument import Argument

class Float(Argument):
    def implementation(self, original_value: str):
        if original_value == None:
            return None

        return float(original_value)
