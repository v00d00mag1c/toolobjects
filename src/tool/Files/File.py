from App.Objects.Object import Object
from pydantic import Field, field_serializer
from pathlib import Path
import secrets

class File(Object):
    path: str = Field(default = None)
    path_hidden: bool = Field(default = False)
    name: str = Field(default = None)
    ext: str = Field(default = None)
    size: int = Field(default = 0)
    stat: dict = Field(default = {})
    # is_common: bool = Field(default = True)

    def countStats(self):
        path = Path(self.path)
        stat = path.stat()

        self.name = path.name
        self.size = stat.st_size
        # self.stat = dict(stat)

    @staticmethod
    def fromPath(path: Path):
        from Files.Dir import Dir
        from Files.FileType import FileType

        item = FileType()
        if path.is_dir() == True:
            item.file = Dir(
                path = str(path)
            )
        else:
            item.file = File(
                path = str(path)
            )

        item.file.countStats()

        return item

    def getParent(self):
        _upper = Path(self.path)

        return _upper.parent

    def getPath(self) -> Path:
        return Path(self.path).joinpath(self.name)

    def get_name_only(self) -> str:
        return self.name.replace('.'+self.ext, '')

    def getContent(self):
        return [self.to_json()]

    def toStorageUnit(self):
        from App.Storage.StorageUnit import StorageUnit

        _bytes = 32
        _hash = secrets.token_hex(_bytes)
        _new = StorageUnit()
        _new.hash = _hash
        _new.fromFile(self.getPath())

        return _new

    @field_serializer('path')
    def path_get(self, path: str) -> str:
        if self.path_hidden == True:
            return None

        return path
