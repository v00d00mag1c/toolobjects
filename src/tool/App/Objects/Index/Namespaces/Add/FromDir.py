from App.Objects.Act import Act
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Argument import Argument
from App.Objects.Arguments.Assertions.NotNone import NotNone
from Data.Types.Boolean import Boolean
from Data.Types.String import String
from App import app
from pathlib import Path
import shutil

from App.Objects.Index.Namespaces.Add.Add import Add

class FromDir(Act):
    @classmethod
    def _arguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
            Argument(
                name = 'dir',
                orig = String,
                default = None
            ),
            Argument(
                name = 'copy',
                orig = Boolean,
                default = False
            )
        ],
        missing_args_inclusion = True)

    async def _implementation(self, i):
        _path = Path(i.get('dir'))
        _new_dir = _path
        _name = _path.name

        if i.get('name') != None:
            _name = i.get('name')

        if i.get('copy'):
            _namespaces_dir = app.app.src.joinpath('namespaces')
            _namespaces_dir.mkdir(exist_ok = True)
            _new_dir = _namespaces_dir.joinpath(_name)
            _new_dir.mkdir(exist_ok = False)

            shutil.copytree(str(_path), str(_new_dir), dirs_exist_ok = True)

        i.set('add_path', str(_new_dir))
        i.set('name', _name)

        await Add().execute(i)
