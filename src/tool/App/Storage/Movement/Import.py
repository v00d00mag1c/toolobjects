from App.Objects.Executable import Executable
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Argument import Argument
from Data.Types.String import String
from Data.Types.Boolean import Boolean
from App.Objects.Arguments.Assertions.NotNone import NotNone
from App.Storage.Item.StorageItem import StorageItem
from App.Storage.Item.Mount import Mount
from App.Objects.Responses.AnyResponse import AnyResponse
from App import app
from pathlib import Path
import zipfile
import datetime

class Import(Executable):
    '''
    Mounts StorageItem from dir
    '''

    @classmethod
    def _arguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
            Argument(
                name = 'path',
                assertions = [NotNone()],
                default = None,
                orig = String
            ),
            Argument(
                name = 'mount_name',
                default = None,
                orig = String
            ),
            Argument(
                name = 'tmp_extract',
                default = None,
                orig = String
            ),
            Argument(
                name = 'as_zip',
                default = False,
                orig = Boolean
            )
        ])

    async def _implementation(self, i):
        path = Path(i.get('path'))
        _dir = path
        _tmp = i.get('tmp_extract')

        _exports = app.app.src.joinpath('exports')
        _exports.mkdir(exist_ok = True)

        if i.get('as_zip') == True:
            if _tmp == None:
                # _tmp_name = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
                #_tmp = app.app.storage.joinpath('tmp').joinpath(datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))
                _tmp_name = path.name
                _tmp = _exports.joinpath(_tmp_name)

            if _tmp.exists() == False:
                _tmp.mkdir(exist_ok = True)
                with zipfile.ZipFile(path, "r") as zip_ref:
                    zip_ref.extractall(_tmp)
            else:
                self.log('tmp export dir with this name is already exists')

            _dir = _tmp

        mount_name = i.get('mount_name')
        if mount_name == None:
            mount_name = _dir.parts[-1]

        _storage = app.Storage.get(mount_name)
        assert _storage == None, 'storage with this name already exists'

        _mount = StorageItem(
            name = mount_name,
            storage = {
                'directory': str(_dir)
            }
        )
        _mount._init_hook()

        await Mount().execute({
            'item': _mount
        })

        #if _tmp == None:
        #    shutil.rmtree(_tmp)

        return AnyResponse(data = _mount)
