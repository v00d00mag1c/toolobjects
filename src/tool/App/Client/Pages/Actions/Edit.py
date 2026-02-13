from App.Client.Displayment import Displayment
from App.Objects.Operations.Edit.Local import Local as LocalEdit
import aiohttp_jinja2
import aiohttp

class Edit(Displayment):
    for_object = 'App.Objects.Operations.Edit.Local'

    async def render_as_page(self, args = {}):
        query = self.request.rel_url.query
        render_as = query.get('as')
        path_val = query.get('item')
        item = self.get_objs([path_val])[0]

        assert item != None, 'not found'

        if render_as != None:
            edit_display = self.get_for(render_as)

            try:
                assert edit_display != None, 'non-editable'

                edit_display = edit_display(request = self.request, context = self.context)

                results = await edit_display.render_as_edit(item, {})
                assert results != None

                return results
            except AssertionError as e:
                self.throw_message('no edit displayment')

        custom_saved_via = list()
        for object_name in item.local_obj.saved_via:
            custom_saved_via.append(object_name.object_name)

        self.context.update({
            'item': item,
            'custom_saved_via': custom_saved_via
        })

        if self.is_post():
            _dict = {'object': item}
            vals = await self.request.post()
            _dict.update(dict(vals))
            await LocalEdit().execute(_dict)

            return self.redirect('/?i=App.Objects.Object&uuids='+path_val)

        return self.render_template("Actions/edit.html")
