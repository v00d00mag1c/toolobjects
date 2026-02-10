from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Argument import Argument
from App.Objects.Arguments.Assertions.NotNone import NotNone
from Data.Types.Boolean import Boolean
from Data.Types.String import String
from App import app
from pathlib import Path
import shutil

from App.Objects.Index.Namespaces.Add.Add import Add

class FromDir(Add):
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
            ),
        ],
        missing_args_inclusion = True)

    async def _implementation(self, i):
        self.check_confirm(i.get('confirm'))

        _path = Path(i.get('dir'))
        _new_dir = _path
        _name = _path.name

        if i.get('name') != None:
            _name = i.get('name')

        if i.get('copy'):
            _custom_dir = app.app.cwd.joinpath('Custom')
            _new_dir = _custom_dir.joinpath(_name)
            _new_dir.mkdir(exist_ok = False)

            shutil.copytree(str(_path), str(_new_dir), dirs_exist_ok = True)

        i.set('add_path', str(_new_dir) + '\\objects')
        i.set('name', _name)

        self._install(i)
