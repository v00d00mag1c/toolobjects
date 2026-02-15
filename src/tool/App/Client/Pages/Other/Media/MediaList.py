from App.Client.Displayment import Displayment

class MediaList(Displayment):
    for_object = ['Media.List.List', 'Media.List']

    async def render_as_object(self, args = {}):
        query = self.request.rel_url.query
        uuids = query.get('uuids')
        orig_item = self.get_objs(uuids)[0]
        items = list()
        for link in orig_item.getLinked():
            items.append(link.item)

        self.context.update({
            'items': items,
            'args': args,
            'hasattr': hasattr
        })
        return self.render_string('Other/Media/media_list.html')

    async def render_as_collection(self, orig_items, args, orig_collection = None):
        self.context.update({
            'items': orig_items,
            'args': args,
            'hasattr': hasattr
        })
        return self.render_string('Other/Media/media_list.html')
