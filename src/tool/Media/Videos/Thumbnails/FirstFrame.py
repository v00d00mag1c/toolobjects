from App.Objects.Thumbnail import Thumbnail
from Media.Videos.Video import Video

class FirstFrame(Thumbnail):
    thumb_for = Video

    async def _implementation(self, i):
        video = i.get('object')

