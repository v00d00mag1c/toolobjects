from App.Objects.Extractor import Extractor
from App.Objects.Object import Object
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Assertions.NotNone import NotNone
from App.Objects.Arguments.Argument import Argument
from App.Storage.StorageUnit import StorageUnit
from Media.Images.Image import Image
from Data.Types.String import String
from Data.Types.Boolean import Boolean
from pathlib import Path
from App import app
import shutil
import os

class ByPath(Extractor):
    @classmethod
    def _arguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
            Argument(
                name = 'object',
                orig = Object,
                assertions = [NotNone()]
            ),
            Argument(
                name = 'path',
                orig = String,
                assertions = [NotNone()]
            ),
            Argument(
                name = 'symlink',
                orig = Boolean,
                default = False
            )
        ])

    async def _implementation(self, i):
        path = Path(i.get('path'))
        assert path.is_dir() == False, 'is dir'
        assert path.exists() == True, 'not exists'

        _unit = app.Storage.get('tmp').get_storage_adapter().get_storage_unit()
        _new_dir = _unit.get_root()

        if i.get('symlink') == True:
            try:
                os.symlink(str(path), str(_new_dir) + '\\' + path.name)
            except OSError as e:
                self.log_error('not enough rights to do symlink')
                self.fatal(e)
        else:
            shutil.copy(str(path), str(_new_dir))

        _new_file = _new_dir.joinpath(path.name)

        _unit.setCommonFile(_new_file)
        _obj = i.get('object')()
        _obj.set_storage_unit(_unit)

        self.append(_obj)
