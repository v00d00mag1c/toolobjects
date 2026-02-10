from App.Objects.Convertation import Convertation
from App.Objects.Relations.Submodule import Submodule
from App.Objects.Responses.ObjectsList import ObjectsList
from Media.Files.File import File
from Media.Text.Text import Text
from App import app

class TextToFile(Convertation):
    @classmethod
    def _submodules(cls) -> list[Submodule]:
        return [
            Submodule(
                item = Text,
                role = ['object_in']
            ),
            Submodule(
                item = File,
                role = ['object_out']
            )
        ]

    def _implementation(self, i):
        _orig = i.get('orig')
        _storage = app.Storage.get('tmp')
        _unit = _storage.get_storage_adapter().get_storage_unit()

        _file = open(str(_unit.getDir().joinpath('text.txt')), 'w', encoding='utf-8')
        _file.write(_orig.value)
        _file.flush()
        _file.close()

        return ObjectsList(items = [_unit])
