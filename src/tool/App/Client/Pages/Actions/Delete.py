from App.Client.Displayment import Displayment

class Delete(Displayment):
    for_object = 'App.Storage.Movement.Delete'

    async def render_as_page(self):
        query = self.request.rel_url.query
        path_val = query.get('item')
        item = self.get_objs([path_val])[0]

        assert item != None, 'not found'

        uuids = [item.getDbIds()]

        self.context.update({
            'item': item,
            'uuids': uuids
        })

        if self.request.method == 'POST':
            _info = await self.request.post()
            item.delete(_info.get('remove_links') == 'on')

            return self.redirect('/?i=App.DB.Search&storage=' + item.getDbName())

        return self.render_template("Actions/delete.html")
