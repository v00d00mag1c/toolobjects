from App.Objects.Object import Object
from Files.File import File
from pydantic import Field

class FileType(Object):
    file: File = Field(default = None)
