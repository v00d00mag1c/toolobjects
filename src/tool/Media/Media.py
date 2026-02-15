from Media.Files.FileType import FileType
from typing import ClassVar
from Web.HTTP.RequestHeaders import RequestHeaders
from App.Objects.Relations.Submodule import Submodule
from App.Objects.Operations.Create.CreationItem import CreationItem
from App import app

class Media(FileType):
    '''
    "Media" is supposed to be a single file with binary contents
    '''

    media_type: ClassVar[str] = ''
    thumbnail_type: ClassVar[list[str]] = []
    default_name: ClassVar[str] = ''
    headers: ClassVar[RequestHeaders] = None # Headers that will be used in media.get
    mime_type: ClassVar[str] = ''
    extensions: ClassVar[list[str]] = []
    cover_extensions: ClassVar[list[str]] = []

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
    def get_page_js_return_function(cls):
        return """
        for (let i = 0; i < elements.length; i++) {
            element = elements[i];
            let src = '';
            let tagName = element.tagName;
            if (element.src) {
                if (element.src.startsWith('data:')) {
                    continue;
                }

                src = element.src;
            }
            """+cls.get_page_js_insert_function()+"""
            if (!src || src == '') {
                continue;
            }

            urls.push({
                'src': src,
                'tagName': tagName
            });
        }

        return urls;
        """

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

    def fill_info_by_path(self, path):
        self.obj.name = path.name

    @classmethod
    async def get_thumbnail_for_collection(self, path):
        return []

    @classmethod
    async def convert_page_results(cls, i, results: dict):
        from Media.Download import Download

        urls = list()
        for item in results:
            urls.append(item.get('src'))

        _vals = i.getValues()
        _vals['url'] = urls

        return await Download().execute(_vals)

    @classmethod
    async def from_url(cls, url: str):
        new = cls()
        _unit = app.Storage.get('tmp').get_storage_adapter().get_storage_unit()
        item = app.DownloadManager.addURL(url, _unit, cls.default_name)
        await item.start()

        new.set_storage_unit(_unit)
        new.save()

        return new

    @classmethod
    def _creations(cls) -> list:
        return [
            CreationItem(
                name = 'Media',
                object_name = 'Media.Media',
                create = 'Media.Get'
            ),
        ]

    @classmethod
    def detect_from_su(cls, storage_unit):
        return cls
