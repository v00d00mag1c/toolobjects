from App.Client.Displayment import Displayment
from App import app

class CreateAbstract(Displayment):
    for_object = 'App.Objects.Misc.Abstract.Create'

    async def render_as_page(self, args = {}):
        query = self.request.rel_url.query
        orig_item = self.get_link_item()

        assert orig_item != None

        self.context['ref'] = query.get('ref')

        if self.is_post():
            data = await self.request.post()
            fields = dict()

            for key, item in data.items():
                if key.startswith('field_'):
                    fields[key.replace('field_', '')] = item

            new_items = await self._execute('App.Objects.Misc.Abstract.Create', {
                'fields': fields,
                'prototype': data.get('prototype_name'),
            })
            new_item = new_items.items[0]

            self._flush_creation(orig_item, new_item)

            return self.redirect('/?i=App.Objects.Object&uuids=' + new_item.getDbIds())

        return self.render_template('Other/Collections/create_abstract.html')
