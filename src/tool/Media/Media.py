from Media.Files.FileType import FileType
from abc import abstractmethod
from typing import ClassVar

class Media(FileType):
    default_name: ClassVar[str] = ''
