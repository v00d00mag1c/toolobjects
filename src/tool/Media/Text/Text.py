from Media.Media import Media
from App.Objects.Relations.LinkInsertion import LinkInsertion
from pydantic import Field, computed_field
from App.Objects.Relations.Submodule import Submodule

class Text(Media):
    value: str | LinkInsertion = Field(default = '')
    has_set_from_file: bool = Field(default = False)

    @computed_field
    @property
    def text(self):
        if self.has_set_from_file:
            return self.value
        else:
            return self.get_file().read()

    @classmethod
    def _submodules(cls) -> list:
        from Media.Text.TextToFile import TextToFile
        from Media.Text.Get import Get
        from Media.Text.ByPath import ByPath

        return [
            Submodule(
                item = TextToFile,
                role = ['convertation']
            ),
            Submodule(
                item = Get,
                role = ['wheel']
            ),
            Submodule(
                item = ByPath,
                role = ['wheel']
            )
        ]
