from ...Arguments.Argument import Argument

class Boolean(Argument):
    def implementation(self, original_value: str):
        return int(original_value) == 1
