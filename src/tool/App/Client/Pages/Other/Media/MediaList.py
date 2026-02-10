from App.Client.Displayment import Displayment

class MediaList(Displayment):
    for_object = ['Media.List.List', 'Media.List']

    async def render_as_collection(self, orig_items, args, orig_collection = None):
        self.context.update({
            'items': orig_items,
            'args': args,
            'hasattr': hasattr
        })
        return self.render_string('Other/Media/media_list.html')
