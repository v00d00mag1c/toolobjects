from Media.Media import Media
from Media.Images.Image import Image
from Media.Videos.Video import Video
from Media.Audios.Audio import Audio
from Media.Text.Text import Text

class Auto(Media):
    @classmethod
    def detect_from_su(cls, storage_unit):
        for class_val in [Image, Video, Audio, Text]:
            if storage_unit.get_ext() in class_val.extensions:
                return class_val

        return Media
