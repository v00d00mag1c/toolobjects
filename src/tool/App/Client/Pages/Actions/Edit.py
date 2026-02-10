from App.Client.Displayment import Displayment
from App.Objects.Operations.Edit.Local import Local as LocalEdit
import aiohttp_jinja2
import aiohttp

class Edit(Displayment):
    for_object = 'App.Objects.Operations.Edit.Local'

    async def render_as_page(self):
        query = self.request.rel_url.query
        vals = await self.request.post()
        path_val = query.get('item')
        item = self.get_objs([path_val])[0]

        assert item != None, 'not found'

        custom_saved_via = list()
        for object_name in item.local_obj.saved_via:
            custom_saved_via.append(object_name.object_name)

        self.context.update({
            'item': item,
            'custom_saved_via': custom_saved_via
        })

        if self.request.method == 'POST':
            _dict = {'object': item}
            _dict.update(dict(vals))
            await LocalEdit().execute(_dict)

            return self.redirect('/?i=App.Objects.Object&uuids='+path_val)

        return self.render_template("Actions/edit.html")
