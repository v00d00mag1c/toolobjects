from App.Objects.Arguments.Argument import Argument
from pydantic import Field
from typing import Generator, Any
from Data.Types.JSON import JSON
from App.Storage.StorageUUID import StorageUUID

class ListArgument(Argument):
    allow_commas_fallback: bool = Field(default = True)
    single_recommended: bool = Field(default = False)
    total_count: int = Field(default=0)

    def getImplementation(self, val: Any | str) -> Any:
        results = list()
        if type(val) == str:
            if JSON.isStringValidJson(val) == True:
                val = JSON.fromText(val).data
            else:
                if self.allow_commas_fallback:
                    val = val.split(',')

        if val == None:
            return []

        if type(val) != list:
            self.log("list argument but not list passed")
            val = [val]

        for item in val:
            #yield self._implementation(val = item)
            results.append(self._implementation(val = item))

        return results

    def getCount(self):
        return len(self.current)

    def getCompleteness(self):
        return self.getCount() / self.total_count

    def append(self, item):
        self.current.append(item)
