from Media.Media import Media
from App.Objects.Relations.LinkInsertion import LinkInsertion
from pydantic import Field, computed_field
from App.Objects.Relations.Submodule import Submodule
from Web.HTTP.RequestHeaders import RequestHeaders
from Data.Types.String import String

class Text(Media):
    value: str | LinkInsertion = Field(default = '')
    has_set_from_file: bool = Field(default = False)
    encoding: str = Field(default = None)
    mime_type = 'text/html'
    default_name = 'text.txt'
    thumbnail_type = ['text']

    _unserializable_on_output = ['value']

    @computed_field
    @property
    def text(self) -> str:
        if self.has_set_from_file:
            return self.value
        else:
            return self.get_file().getPath().read_text(encoding = self.encoding)

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

    def _display_as_string(self):
        return String.cut(str(self.text), 500)
