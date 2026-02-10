from Media.Files.FileType import FileType
from typing import ClassVar
from Web.HTTP.RequestHeaders import RequestHeaders
from App.Objects.Relations.Submodule import Submodule

class Media(FileType):
    '''
    "Media" is supposed to be a single file with binary contents
    '''

    thumbnail_type: ClassVar[list[str]] = []
    default_name: ClassVar[str] = ''
    headers: ClassVar[RequestHeaders] = None # Headers that will be used in media.get
    mime_type: ClassVar[str] = ''

    @classmethod
    def _submodules(cls) -> list:
        from Media.Download import Download
        from Media.ByStorageUnit import ByStorageUnit
        from Media.ByPath import ByPath
        
        return [
            Submodule(
                item = Download,
                role = ['media_method', 'wheel']
            ),
            Submodule(
                item = ByStorageUnit,
                role = ['media_method', 'wheel']
            ),
            Submodule(
                item = ByPath,
                role = ['media_method', 'wheel']
            )
        ]
