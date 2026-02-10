from App.Client.Displayment import Displayment
from Data.Primitives.Collections.Create import Create as RealCreate
from App import app

class Create(Displayment):
    for_object = 'Data.Primitives.Collections.Create'

    async def render_as_page(self, args = {}):
        query = self.request.rel_url.query
        storage = app.Storage.get(query.get('storage'))

        assert storage != None, 'storage not found'

        self.context.update({
            'storage': storage,
            'ref': query.get('ref')
        })

        if self.is_post():
            data = await self.request.post()

            root = storage.get_root_collection()
            new_items = await RealCreate().execute({
                'name': data.get('name'),
                'collection_type': data.get('prototype'),
            })
            new_item = new_items.items[0]
            new_item.local_obj.make_public()
            new_item.flush(storage)
            if root:
                root.link(new_item)

            new_item.save()

            return self.redirect('/?i=App.Objects.Object&uuids=' + new_item.getDbIds())

        return self.render_template('Other/Collections/create.html')
