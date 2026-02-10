from App.Objects.Object import Object

class Dict(Object):
    @classmethod
    def asArgument(cls, val: dict):
        if type(val) == dict:
            return val

        return super().asArgument(val)
