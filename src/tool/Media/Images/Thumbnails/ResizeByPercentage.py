from App.Objects.Thumbnail import Thumbnail
from Media.Images.Image import Image
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Argument import Argument
from App.Objects.Responses.ObjectsList import ObjectsList
from Data.Types.Float import Float

class ResizeByPercentage(Thumbnail):
    thumb_for = Image

    @classmethod
    def _arguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
            Argument(
                name = 'percentage',
                orig = Float,
                default = 0.5
            )
        ])

    async def _implementation(self, i):
        image = i.get('object')
        thumb = image._resize_by_percentage(image._read_file(), i.get('percentage'))

        image.link(thumb.obj, role = ['thumbnail'])
        image._reset_file()

        return ObjectsList(items = [image])
