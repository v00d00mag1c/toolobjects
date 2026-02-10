from App.Objects.Act import Act
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Argument import Argument
from Data.Types.String import String
from App.Objects.Index.Namespaces.Add.Add import Add
from App import app
from pathlib import Path

class FromZip(Act):
    @classmethod
    def _arguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
            Argument(
                name = 'path',
                orig = String,
                default = None
            )
        ],
        missing_args_inclusion = True)

    async def _implementation(self, i):
        _path = Path(i.get('path'))
        _namespaces_dir = app.app.src.joinpath('namespaces')
        _namespaces_dir.mkdir(exist_ok = True)
        _new_dir = _namespaces_dir.joinpath(_path.name)
        _new_dir.mkdir(exist_ok = False)

        await Add().execute(i)
