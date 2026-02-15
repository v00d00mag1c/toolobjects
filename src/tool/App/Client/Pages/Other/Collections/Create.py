from App.Client.Displayment import Displayment
from Data.Primitives.Collections.Create import Create as RealCreate
from App import app

class Create(Displayment):
    for_object = ['Data.Primitives.Collections.Create']

    async def render_as_page(self, args = {}):
        query = self.request.rel_url.query
        item = self.get_link_item()

        assert item != None

        self.context['ref'] = query.get('ref')

        if self.is_post():
            data = await self.request.post()

            new_items = await self._execute(self.for_object[0], {
                'name': data.get('name'),
                'collection_type': data.get('prototype'),
            })
            new_item = new_items.items[0]

            self._flush_creation(item, new_item)

            return self.redirect('/?i=App.Objects.Object&uuids=' + new_item.getDbIds())

        return self.render_template('Other/Collections/create.html')
