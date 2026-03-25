from App.Objects.Act import Act
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Responses.ObjectsList import ObjectsList
from App.Objects.Arguments.Assertions.NotNone import NotNone
from App.Objects.Arguments.Argument import Argument
from Data.Types.Boolean import Boolean
from Data.Types.String import String
from typing import ClassVar

class Search(Act):
    self_name: ClassVar[str] = "Search"

    @classmethod
    def _arguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
            Argument(
                name = 'as_result_items',
                orig = Boolean,
                default = False
            ),
            Argument(
                name = 'q',
                orig = String,
                default = None
            )
        ])
