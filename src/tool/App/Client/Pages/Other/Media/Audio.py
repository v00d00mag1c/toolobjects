from App.Client.Displayment import Displayment
from Data.Types.String import String

class Audio(Displayment):
    for_object = 'Media.Audios.Audio'

    async def render_as_object(self, item):
        self.context.update({
            'items': [item],
        })

        return self.render_string('Other/Media/audio_page.html')

    async def render_as_collection(self, orig_items, args, orig_collection = None):
        self.context.update({
            'items': orig_items,
            'show_id': True
        })
        return self.render_string('Other/Media/audio_page.html')
