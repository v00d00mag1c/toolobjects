from App.Objects.Object import Object
from pydantic import Field
from urllib.parse import urlparse

class URL(Object):
    value: str = Field()

    @classmethod
    def asArgument(cls, val):
        if val == None:
            return None

        return str(val)

    def get_path(self):
        return urlparse(self.value).path

    def get_filename(self) -> str:
        _path = self.get_path().split('/')
        _name = _path[-1]
        if len(_name.split('.')) == 1:
            return None

        return _name

    async def download_function(self, dir: str):
        pass
