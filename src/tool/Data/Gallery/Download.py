from App.Objects.Extractor import Extractor
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Assertions.NotNoneAssertion import NotNoneAssertion
from App.Objects.Arguments.Argument import Argument
from Data.String import String
from Data.Boolean import Boolean
from Files.FileTypes.Image import Image
from Data.Gallery.Gallery import Gallery
from App.Objects.Misc.Source import Source
from Web.URL import URL
from App import app

class Download(Extractor):
    @classmethod
    def getArguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
            Argument(
                name = 'url',
                orig = String,
                assertions = [NotNoneAssertion()]
            ),
            Argument(
                name = 'gallery',
                id_allow = True,
                orig = Gallery
            ),
            Argument(
                name = 'filename',
                orig = String,
            ),
            Argument(
                name = 'download',
                default = True,
                orig = Boolean
            )
        ])

    async def implementation(self, i):
        _url = URL(
            value = i.get('url')
        )
        filename = i.get('filename')
        gallery = i.get('gallery')
        if filename == None:
            filename = _url.get_filename()

        image = Image()

        if i.get('download') == True:
            _unit = app.Storage.get('tmp').getStorageUnit()

            item = app.DownloadManager.addURL(_url.value, _unit, filename)
            await item.start()

            image.set_storage_unit(_unit)

        image.obj.make_public()
        image.obj.set_common_source(Source(
            obj = _url
        ))

        if gallery != None:
            gallery.link(image)

        self.append(image)
