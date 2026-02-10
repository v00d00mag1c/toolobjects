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
    extensions: ClassVar[list[str]] = []

    @classmethod
    def get_headers(cls):
        headers = RequestHeaders()
        headers.accept = cls.mime_type
        headers.content_type = cls.mime_type

        return headers

    @classmethod
    def get_page_js_selectors(cls):
        return []

    @classmethod
    def get_page_js_function(cls):
        return ''

    @classmethod
    def get_page_js_insert_function(cls):
        return ''

    @classmethod
    def _submodules(cls) -> list:
        from Media.Download import Download
        from Media.ByStorageUnit import ByStorageUnit
        from Media.ByPath import ByPath
        from Media.ByDir import ByDir
        from Media.FromPage import FromPage

        returns = list()

        for item in [Download, ByStorageUnit, ByPath, ByDir, FromPage]:
            returns.append(Submodule(
                item = item,
                role = ['media_method', 'wheel']
            ))

        return returns
