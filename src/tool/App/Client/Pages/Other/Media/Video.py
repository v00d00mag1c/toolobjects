from App.Client.Displayment import Displayment
from Data.Types.String import String

class Video(Displayment):
    for_object = 'Media.Videos.Video'

    async def render_as_object(self, item):
        self.context.update({
            'items': [item],
        })

        return self.render_string('Other/Media/video.html')

    async def render_as_list_item(self, item, args):
        self.context.update({
            'items': [item],
        })

        return self.render_string('Other/Media/video.html')
