from App.Objects.Extractor import Extractor
from App.Objects.Object import Object
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Assertions.NotNone import NotNone
from App.Objects.Arguments.Argument import Argument
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
            Argument(
                name = 'url',
                orig = String,
                assertions = [NotNone()]
            ),
            Argument(
                name = 'filename',
                orig = String,
            ),
            Argument(
                name = 'download',
                default = True,
                orig = Boolean
            ),
        ])

    async def _implementation(self, i):
        _url = URL(
            value = i.get('url')
        )
        _obj = i.get('object')
        filename = i.get('filename')
        if filename == None:
            filename = _url.get_filename()
            if filename == None:
                filename = _obj.default_name

        _item = _obj()
        if i.get('download') == True:
            _unit = app.Storage.get('tmp').get_storage_adapter().get_storage_unit()

            item = app.DownloadManager.addURL(_url.value, _unit, filename)
            await item.start({
                'Content-Type': 'image/jpeg'
            })

            _item.set_storage_unit(_unit)

        _item.obj.set_common_source(Source(
            obj = _url
        ))

        self.append(_item)
