from App.Objects.Thumbnail import Thumbnail
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Argument import Argument
from App.Objects.Responses.ObjectsList import ObjectsList
from Data.Types.Float import Float
from Data.Types.Int import Int
from Media.Videos.Video import Video
from Media.Images.Image import Image

class Frames(Thumbnail):
    thumb_for = Video

    @classmethod
    def _arguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
            Argument(
                name = 'frame_interval', # in seconds
                orig = Float,
                default = 10,
            ),
            Argument(
                name = 'frames_limit',
                orig = Int,
                default = 1,
            ),
            Argument(
                name = 'duration_offset',
                orig = Int,
                default = 4,
            ),
            Argument(
                name = 'quality',
                orig = Int,
                default = 85,
            )
        ])

    async def _implementation(self, i):
        import av

        video = i.get('object')
        file = video.get_file()

        container = video._read_file()

        stream = container.streams.video[0]
        stream.thread_type = 'AUTO'

        duration_sec = container.duration / av.time_base
        offset = i.get('duration_offset')
        limit = i.get('frames_limit')
        frame_interval = i.get('frame_interval')
        quality = i.get('quality')
        total_thumbs = int(duration_sec / frame_interval)

        items = ObjectsList(items = [])

        for iterator in range(total_thumbs):
            this_thumb_timecode = iterator * frame_interval
            if this_thumb_timecode > duration_sec:
                this_thumb_timecode = duration_sec

            this_thumb_timecode = min(this_thumb_timecode + offset, duration_sec)
            target_time = int(this_thumb_timecode / stream.time_base)
            container.seek(target_time, stream = stream)
            frame = next(container.decode(stream))

            thumb_image = Image()
            thumb_image.move(video)

            img = frame.to_image()
            filename = "{0}_thumb_{1}s.jpg".format(file.getPath().stem, this_thumb_timecode)

            img.save(file.getPath().with_name(filename), quality = quality)

            thumb_image.set_insertion_name(filename)
            thumb_image.save()

            items.append(thumb_image)

            if limit != None and iterator > limit:
                break

        video._reset_file()

        return items
