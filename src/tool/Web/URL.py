from App.Objects.Object import Object
from pydantic import Field
from urllib.parse import urlparse

class URL(Object):
    value: str = Field()

    def get_path(self):
        return urlparse(self.value).path

    def get_filename(self) -> str:
        _path = self.get_path().split('/')

        return _path[-1]
