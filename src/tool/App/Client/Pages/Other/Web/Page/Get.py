from App.Client.Displayment import Displayment
from App.Storage.Item.StorageItem import StorageItem
from App import app

class Get(Displayment):
    for_object = 'Web.Pages.Get'

    async def render_as_page(self, args = {}):
        orig_item = self.get_link_item()

        assert orig_item != None

        self.context.update({
            'item': orig_item,
            'args': args,
        })

        if self.is_post():
            data = await self.request.post()
            url = data.get('url')
            inline_css = data.get('inline_css')
            mode = 'Web.Pages.Crawler.Original'
            if inline_css == 'on':
                mode = 'Web.Pages.Crawler.Plain'

            assert url != '', 'url = null'

            new_items = await self._execute('Web.Pages.Get', {
                'url': url,
                'mode': mode,
            })
            new_item = new_items.items[0]
            self._flush_creation(orig_item, new_item)

            return self.redirect('/?i=App.Objects.Object&uuids=' + new_item.getDbIds())

        return self.render_template('Other/Web/Page/get.html')
