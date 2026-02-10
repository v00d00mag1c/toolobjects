from Media.Media import Media
from App.Objects.Requirements.Requirement import Requirement
from App.Objects.Misc.Thumbnail import Thumbnail
from App.Objects.Relations.Submodule import Submodule
from pathlib import Path

class Image(Media):
    default_name = 'image.jpg'
    mime_type = 'image/jpeg'
    _img = None

    @classmethod
    def _submodules(cls) -> list:
        from Media.Download import Download
        from Media.ByStorageUnit import ByStorageUnit
        from Media.ByPath import ByPath
        from Media.Images.MakeThumbnail import MakeThumbnail

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
            ),
            Submodule(
                item = MakeThumbnail,
                role = ['thumbnail']
            )
        ]

    @classmethod
    def _requirements(cls):
        return [
            Requirement(
                name = 'imageio',
            )
        ]

    def _read_file(self):
        from PIL import Image

        if self._img == None:
            _file = self.get_file()
            if _file == None:
                return None

            self._img = Image.open(str(_file.getPath()))

        return self._img

    def _reset_file(self):
        self._img = None

    def _set_dimensions(self, data):
        self.obj.width = data.size[0]
        self.obj.height = data.size[1]

    def _make_thumbnail(self, data, percentage: float = 0.5):
        sizes = (data.size[0], data.size[1])
        new_sizes = (int(sizes[0] * percentage), int(sizes[1] * percentage))
        resized_img = data.resize(new_sizes)
        resized_img.convert('RGB')

        _thumb_image = Image()
        _thumb_image.move(self)
        _thumb_image._set_dimensions(resized_img)

        filename = Path(data.filename)
        _new_file_name = filename.stem + '_thumb_' + str(percentage) + filename.suffix
        _new_name = filename.with_name(_new_file_name)
        resized_img.save(_new_name)

        _thumb_image.set_insertion_name(_new_file_name)

        return Thumbnail(
            role = ['image'],
            obj = _thumb_image
        )

    def save(self):
        _read = self._read_file()
        self._set_dimensions(_read)
        self._reset_file()

        super().save()
