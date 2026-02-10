from App.Objects.Extractor import Extractor
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Assertions.NotNone import NotNone
from App.Objects.Arguments.Argument import Argument
from Data.Types.String import String
from Data.Types.Boolean import Boolean
from Data.Primitives.Collections.Collection import Collection
from Media.Images.Image import Image
from Media.Images.MakeImageThumbnail import MakeImageThumbnail
from App.Objects.Misc.Source import Source
from Web.URL import URL
from App import app

class Download(Extractor):
    @classmethod
    def _arguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
            Argument(
                name = 'url',
                orig = String,
                assertions = [NotNone()]
            ),
            Argument(
                name = 'list',
                by_id = True,
                orig = Collection
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
            Argument(
                name = 'make_thumbnail',
                default = False,
                orig = Boolean
            )
        ])

    async def _implementation(self, i):
        _url = URL(
            value = i.get('url')
        )
        filename = i.get('filename')
        gallery = i.get('list')
        if filename == None:
            filename = _url.get_filename()
            if filename == None:
                filename = 'image.jpg'

        image = Image()

        if i.get('download') == True:
            _unit = app.Storage.get('tmp').get_storage_adapter().get_storage_unit()

            item = app.DownloadManager.addURL(_url.value, _unit, filename)
            await item.start()

            image.set_storage_unit(_unit)

            _read = image._read_file()
            image._set_dimensions(_read)

            if i.get('make_thumbnail') == True:
                try:
                    _resp = await MakeImageThumbnail().execute({
                        'image': image
                    })
                    image.local_obj.add_thumbnails(_resp.getItems())
                except Exception as e:
                    self.log_error(e, role = ['thumbnail'], exception_prefix = 'Error when making thumbnail: ')

        image._reset_file()
        image.local_obj.make_public()
        image.obj.set_common_source(Source(
            obj = _url
        ))

        if gallery != None:
            gallery.link(image)

        self.append(image)
