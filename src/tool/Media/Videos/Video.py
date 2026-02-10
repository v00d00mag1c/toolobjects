from Media.Media import Media
from Web.HTTP.RequestHeaders import RequestHeaders
from App.Objects.Relations.Submodule import Submodule
from App.Objects.Requirements.Requirement import Requirement
from typing import ClassVar

class Video(Media):
    thumbnail_type = ['video']
    default_name = 'video.mp4'
    mime_type = 'video/mp4'
    media_type: ClassVar[str] = 'video'
    _vid = None

    @classmethod
    def _submodules(cls) -> list:
        from Media.Videos.Thumbnails.Frames import Frames

        return [
            Submodule(
                item = Frames,
                role = ['thumbnail']
            )
        ]

    @classmethod
    def _requirements(cls):
        return [
            Requirement(
                name = 'av'
            )
        ]

    def _read_file(self):
        import av

        if self._vid == None:
            _vid = self.get_file()
            if _vid == None:
                return None

            self._vid = av.open(str(_vid.getPath()))

        return self._vid

    def _reset_file(self):
        self._vid.close()
        self._vid = None

    def _set_dimensions(self, vid):
        import av

        video_stream = next(s for s in vid.streams if s.type == 'video')

        self.obj.width = video_stream.codec_context.width
        self.obj.height = video_stream.codec_context.height

        self.obj.duration = round(vid.duration / av.time_base, 5)

    def save_hook(self):
        if self.obj.has_dimensions() == False:
            _read = self._read_file()
            self._set_dimensions(_read)
            self._reset_file()
