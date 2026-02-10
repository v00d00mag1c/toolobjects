from App.Objects.Object import Object
from Data.Types.JSON import JSON

class Dict(Object):
    @classmethod
    def asArgument(cls, val: dict):
        if type(val) == dict:
            return val

        if type(val) == str:
            return JSON.fromText(val).data

        return super().asArgument(val)
