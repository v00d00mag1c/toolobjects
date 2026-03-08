from App.Client.Displayment import Displayment

class MediaList(Displayment):
    for_object = ['Media.List.List', 'Media.List']
    prefer_object_displayment = 'page'

    async def render_as_page(self, args = {}):
        return await self.render_as_object({
            'redirect': True
        })

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

        if args.get('redirect') == True:
            return self.redirect('/?i=App.DB.Search&storage={0}&act=linked_to&linked_to_type=item&linked_to={1}'.format(items[0].getStorageName(), items[0].getDbIds()))

        return self.render_string('Other/Media/media_list.html')

    async def render_as_collection(self, orig_items, args, orig_collection = None):
        self.context.update({
            'items': orig_items,
            'args': args,
            'hasattr': hasattr
        })
        return self.render_string('Other/Media/media_list.html')
