from App.Objects.Arguments.Argument import Argument
from pydantic import Field
from typing import Generator, Any
from Data.JSON import JSON

class ListArgument(Argument):
    allow_commas_fallback: bool = Field(default = True)
    single_recommended: bool = Field(default = False)
    total_count: int = Field(default=0)
    allow_commas_fallback: bool = Field(default=True)

    def implementation(self, val: Any | str) -> Any:
        return list(self.getListValue(val))

    def getCount(self):
        return len(self.current)

    def getCompleteness(self):
        return self.getCount() / self.total_count

    def append(self, item):
        self.current.append(item)

    def getListValue(self, original_value: str | list) -> Generator[Any]:
        if type(original_value) == str:
            if JSON.isStringValidJson(original_value) == True:
                original_value = JSON.fromText(original_value).data
            else:
                if self.allow_commas_fallback:
                    original_value = original_value.split(',')

        if original_value == None:
            return None

        for item in original_value:
            yield self.getOrig().asArgument(val = item)
