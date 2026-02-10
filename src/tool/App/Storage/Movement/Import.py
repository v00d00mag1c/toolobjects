from App.Objects.Executable import Executable
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Argument import Argument
from Data.String import String
from Data.Boolean import Boolean
from App.Objects.Arguments.Assertions.NotNoneAssertion import NotNoneAssertion
from App.Storage.StorageItem import StorageItem
from App.Responses.AnyResponse import AnyResponse
from App import app
from pathlib import Path

class Import(Executable):
    '''
    Mounts StorageItem from dir
    '''

    @classmethod
    def getArguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
            Argument(
                name = 'path',
                assertions = [NotNoneAssertion()],
                default = None,
                orig = String
            ),
            Argument(
                name = 'mount_name',
                default = None,
                orig = String
            ),
            Argument(
                name = 'as_zip',
                default = False,
                orig = Boolean
            )
        ])

    async def implementation(self, i):
        path = Path(i.get('path'))
        as_zip = i.get('as_zip')
        mount_name = i.get('mount_name')
        if mount_name == None:
            mount_name = path.parts[-1]

        _storage = app.Storage.get(mount_name)
        assert _storage == None, 'storage with this name already exists'

        _mount = StorageItem(
            name = mount_name,
            directory = str(path)
        )

        app.Storage.append(_mount)

        self.log(f"mounted storage {mount_name}")

        return AnyResponse(data = _mount)
