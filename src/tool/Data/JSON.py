from App.Objects.Object import Object
from pydantic import Field
from Data.DictList import DictList
# from Plugins.App.Objects.Arguments.Assertions.NotNoneAssertion import NotNoneAssertion

import json

class JSON(Object):
    data: list | dict | str = Field(default = None)

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
