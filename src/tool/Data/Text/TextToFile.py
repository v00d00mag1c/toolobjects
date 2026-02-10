from App.Objects.Convertation import Convertation
from App.Objects.Relations.Submodule import Submodule
from App.Objects.Responses.ObjectsList import ObjectsList
from Files.File import File
from Data.Text.Text import Text
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

    def implementation(self, i):
        _orig = i.get('orig')
        _storage = app.Storage.get('tmp')
        _unit = _storage.getStorageUnit()

        _file = open(str(_unit.getDir().joinpath('text.txt')), 'w', encoding='utf-8')
        _file.write(_orig.value)
        _file.flush()
        _file.close()

        return ObjectsList(items = [_unit])
