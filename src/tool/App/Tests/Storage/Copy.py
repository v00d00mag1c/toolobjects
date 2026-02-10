from App.Objects.Test import Test
from App.Storage.Movement.Copy.Files import Files
from App import app

class Copy(Test):
    async def implementation(self, i):
        _files = Files()
        _storage = app.app.storage.joinpath('test')
        _storage.mkdir(exist_ok = True)
        await _files.execute({
            'items': ['common_7412202858935877632'],
            'directory': _storage
        })
