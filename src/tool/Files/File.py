from App.Objects.Object import Object
from pydantic import Field
from pathlib import Path

class File(Object):
    path: str = Field(default = None)
    name: str = Field(default = None)
    size: int = Field(default = 0)
    stat: dict = Field(default = {})

    def constructor(self):
        path = Path(self.path)
        stat = path.stat()

        self.name = path.name
        self.size = stat.st_size
        # self.stat = dict(stat)

    def getParent(self):
        _upper = Path(self.path)

        return _upper.parent

    def getContent(self):
        return [self.to_json()]
