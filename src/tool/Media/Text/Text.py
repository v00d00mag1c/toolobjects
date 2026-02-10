from Media.Media import Media
from App.Objects.Relations.LinkInsertion import LinkInsertion
from pydantic import Field, computed_field
from App.Objects.Relations.Submodule import Submodule
from Web.HTTP.RequestHeaders import RequestHeaders
from Data.Types.String import String
from App.Objects.Responses.ObjectsList import ObjectsList

class Text(Media):
    value: str | LinkInsertion = Field(default = '')
    has_set_from_file: bool = Field(default = True)
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
    def get_page_js_selectors(cls):
        return ['span', 'p']

    @classmethod
    def get_page_js_return_function(cls):
        return """
        for (let i = 0; i < elements.length; i++) {
            element = elements[i];
            let src = element.innerText;
            let tagName = element.tagName;
            if (!src || src == '') {
                continue;
            }

            urls.push({
                'text': src,
                'tagName': tagName
            });
        }

        return urls;
        """

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

    @classmethod
    async def convert_page_results(cls, i, results: dict):
        _objs = ObjectsList(items = [])
        for item in results:
            _objs.append(Text(
                value = item.get('text')
            ))

        return _objs
