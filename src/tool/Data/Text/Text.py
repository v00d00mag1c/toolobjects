from App.Objects.Object import Object
from App.Objects.Relations.LinkInsertion import LinkInsertion
from pydantic import Field
from App.Objects.Relations.Submodule import Submodule

class Text(Object):
    value: str | LinkInsertion = Field(default = '')

    @classmethod
    def _submodules(cls) -> list:
        from Data.Text.TextToFile import TextToFile

        return [
            Submodule(
                item = TextToFile,
                role = ['convertation']
            )
        ]
