from Media.Files.FileType import FileType
from typing import ClassVar
from Web.HTTP.RequestHeaders import RequestHeaders

class Media(FileType):
    '''
    "Media" is supposed to be a single file with binary contents
    '''

    thumbnail_type: ClassVar[list[str]] = []
    default_name: ClassVar[str] = ''
    headers: ClassVar[RequestHeaders] = None # Headers that will be used in media.get
    mime_type: ClassVar[str] = ''
