from App.Client.Displayment import Displayment
from Data.Types.String import String
from App.Storage.StorageUUID import StorageUUID

class Image(Displayment):
    for_object = 'Media.Images.Image'
    prefer_object_displayment = 'page'

    async def render_as_page(self, args = {}):
        query = dict(self.request.rel_url.query)
        item = args.get('item')
        if item == None:
            item = StorageUUID.fromString(query.get('item')).toPython()

        assert item != None, 'not found image'

        self.context.update({
            'items': [item],
        })

        _url = item.get_url(True, True)
        if _url != None:
            return self.redirect(_url)

        return self.render_template('Other/Media/image.html')

    async def render_as_object(self, item):
        self.context.update({
            'items': [item],
        })

        return self.render_string('Other/Media/image.html')

    async def render_as_list_item(self, item, args):
        self.context.update({
            'items': [item],
        })

        return self.render_string('Other/Media/image.html')
