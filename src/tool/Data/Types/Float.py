from Data.Types.Int import Int

class Float(Int):
    value: float = None

    @classmethod
    def asArgument(cls, val):
        if val == None:
            return None

        return float(val)
