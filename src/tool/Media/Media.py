from Media.Files.FileType import FileType
from abc import abstractmethod
from typing import ClassVar
from Web.HTTP.RequestHeaders import RequestHeaders

class Media(FileType):
    default_name: ClassVar[str] = ''
    headers: ClassVar[RequestHeaders] = None # Headers that will be used in media.get
    mime_type: ClassVar[str] = ''
