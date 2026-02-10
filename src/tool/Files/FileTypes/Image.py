from Files.FileTypes.FileType import FileType
from pydantic import Field
from App.Objects.Requirements.Requirement import Requirement
from App.Objects.Misc.Thumbnail import Thumbnail
from pathlib import Path

class Image(FileType):
    width: int = Field(default = None)
    height: int = Field(default = None)

    @classmethod
    def _required_modules(cls):
        return [
            Requirement(
                name = 'imageio',
            )
        ]

    def _read_file(self):
        from PIL import Image

        return Image.open(str(self.get_file().getPath()))

    def _set_dimensions(self, data):
        self.width = data.size[0]
        self.height = data.size[1]

    def _make_thumbnail(self, data, percentage: float = 0.5):
        sizes = (data.size[0], data.size[1])
        new_sizes = (int(sizes[0] * percentage), int(sizes[1] * percentage))
        resized_img = data.resize(new_sizes)
        #data.convert('RGB')
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
