from Media.Media import Media
from Media.Images.Image import Image
from typing import ClassVar
from pydantic import Field
from App.Objects.Misc.Thumbnail import Thumbnail
from Media.ByPath import ByPath

class Audio(Media):
    mime_type = 'audio/mp3'
    default_name = 'audio.mp3'
    thumbnail_type = ['audio']
    extensions = ['mp3', 'aac']
    media_type: ClassVar[str] = 'audio'
    cover_extensions: ClassVar[str] = ['jpeg', 'jpg']

    performers: list[str] = Field(default = [])

    @classmethod
    def get_thumbnail_for_collection(self, path):
        #await ByPath().execute({})
        #_image = Image()
        return []
