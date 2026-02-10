from App.Objects.Misc.Valueable import Valueable
from Data.Types.JSON import JSON
from pydantic import Field

class List(Valueable):
    value: list = Field(default = None)
    allow_commas_fallback: bool = Field(default = True)
    single_recommended: bool = Field(default = False)

    def asArgumentAsInstance(self, val):
        if val == None:
            # its better in some cases
            return []
            #return None

        results = list()
        if type(val) == str:
            if JSON.isStringValidJson(val) == True:
                val = JSON.fromText(val).data
            else:
                if self.allow_commas_fallback:
                    val = val.split(',')

        if type(val) != list:
            self.log("list argument but not list passed", role = ['validation.not_list'])
            val = [val]

        for item in val:
            _val = self.value[0]
            if callable(_val):
                results.append(_val.asArgument(val = item))
            else:
                results.append(_val.asArgumentAsInstance(val = item))

        return results
