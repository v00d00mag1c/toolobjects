from App.Objects.Object import Object
from pydantic import Field
from App.Objects.Misc.DictList import DictList
# from Plugins.App.Objects.Arguments.Assertions.NotNone import NotNone

import json

class JSON(Object):
    data: list | dict | str = Field(default = None)

    @classmethod
    def asArgument(cls, val):
        if val == None:
            return None

        if type(val) == dict:
            return val

        return cls.fromText(val).data

    @staticmethod
    def fromText(text: str):
        _json = JSON()
        _json.data = json.loads(text)
    
        return _json

    def dump(self, indent = None) -> str:
        return json.dumps(self.data, ensure_ascii = False, indent = indent)

    @staticmethod
    def isStringValidJson(text: str) -> bool:
        #if type(text) != str:
        #    return True

        try:
            _json = json.loads(text)

            return _json != None and type(_json) != int and type(_json) != str
        except json.JSONDecodeError:
            return False
        except TypeError:
            return False
