from App.Client.Displayment import Displayment

class CreateCheckmarks(Displayment):
    for_object = 'Data.Primitives.Checkmarks.CreateList'

    async def render_as_page(self, args = {}):
        query = self.request.rel_url.query
        orig_item = self.get_link_item()

        assert orig_item != None

        self.context['ref'] = query.get('ref')

        if self.is_post():
            data = await self.request.post()

            new_items = await self._execute(self.for_object, {
                'name': data.get('todolist_name')
            })

            return self.redirect(self._flush_creation(orig_item, new_items.items))

        return self.render_template('Other/Collections/create_checkmarks.html')
