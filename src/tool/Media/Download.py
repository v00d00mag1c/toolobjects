from App.Objects.Extractor import Extractor
from App.Objects.Object import Object
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Assertions.NotNone import NotNone
from App.Objects.Arguments.Argument import Argument
from App.Objects.Arguments.ListArgument import ListArgument
from Data.Types.String import String
from Data.Types.Boolean import Boolean
from App.Objects.Misc.Source import Source
from Web.URL import URL
from App import app

class Download(Extractor):
    @classmethod
    def _arguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
            Argument(
                name = 'object',
                orig = Object,
                assertions = [NotNone()]
            ),
            ListArgument(
                name = 'url',
                orig = String,
                assertions = [NotNone()]
            ),
            Argument(
                name = 'filename',
                orig = String,
            ),
            Argument(
                name = 'referer',
                orig = String,
                default = None
            ),
            Argument(
                name = 'download',
                default = True,
                orig = Boolean
            ),
        ])

    async def _implementation(self, i):
        for item in i.get('url'):
            _url = URL(
                value = item
            )
            _obj = i.get('object')
            filename = i.get('filename')
            if filename == None:
                filename = _url.get_filename()
                if filename == None:
                    filename = _obj.default_name

            _su = None
            if i.get('download') == True:
                _su = app.Storage.get('tmp').get_storage_adapter().get_storage_unit()

                item = app.DownloadManager.addURL(_url.value, _su, filename)
                _headers = _obj.get_headers()
                _headers.referer = i.get('referer')

                await item.start(_headers)

            _item = _obj.detect_from_su(_su)
            _item.set_storage_unit(_su)
            _item.obj.set_common_source(Source(
                obj = _url
            ))

            self.append(_item)
