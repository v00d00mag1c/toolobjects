from App.Objects.Arguments.Argument import Argument
from pydantic import Field
from typing import Generator, Any
from Data.Types.JSON import JSON
from App.Storage.StorageUUID import StorageUUID
from Data.Types.List import List

class ListArgument(Argument):
    allow_commas_fallback: bool = Field(default = True)
    single_recommended: bool = Field(default = False)
    total_count: int = Field(default=0)

    def init_hook(self):
        self.orig = List(
            value = [self.orig],
            allow_commas_fallback = self.allow_commas_fallback,
            single_recommended = self.single_recommended
        )

    def _by_id(self, val: str):
        returns = list()

        if type(val) == list:
            for item in val:
                returns.append(super()._by_id(item))
        else:
            returns.append(super()._by_id(val))

        return returns
