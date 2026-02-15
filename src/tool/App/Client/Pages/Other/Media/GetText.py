from App.Client.Displayment import Displayment
from App.Storage.Item.StorageItem import StorageItem

class GetText(Displayment):
    for_object = 'Media.Text.Get'

    async def render_as_page(self, args = {}):
        query = self.request.rel_url.query
        item = self.get_link_item()

        assert item != None
        self.context['ref'] = query.get('ref')

        if self.is_post():
            data = await self.request.post()
            new_items = await self._execute('Media.Text.Get', {
                'object': 'Media.Text',
                'text': data.get('text')
            })
            new_item = new_items.items[0]

            return self.redirect(self._flush_creation(item, new_item))

        return self.render_template('Other/Media/text.html')
