from .Response import Response
from pydantic import Field
from typing import List

class ModelsResponse(Response):
    data: List = Field(default = [])

    def toDict(self) -> list:
        out = []

        for item in self.data:
            if hasattr(item, 'toJson') == False:
                out.append(None)
            else:
                out.append(item.toJson())

        return out
