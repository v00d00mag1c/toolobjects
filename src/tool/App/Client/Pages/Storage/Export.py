from App.Client.Displayment import Displayment
from App.Storage.Movement.Export import Export as RealExport
from App import app

class Export(Displayment):
    for_object = 'App.Storage.Movement.Export'

    async def render_as_page(self, args = {}):
        query = self.request.rel_url.query
        act = query.get('act')
        act = 'storage'
        name = query.get('storage')

        self.context.update({
            'act': act,
            'ref': query.get('ref')
        })
        if act == 'storage':
            storage = app.Storage.get(name)

            assert storage != None

            self.context.update({
                'name': name
            })

            if self.is_post():
                data = await self.request.post()

                await RealExport().execute({
                    'items': storage.adapter.getQuery().toObjectsList(),
                    'as_zip': data.get('as_zip') == 'on'
                })

                return self.redirect('?i=App.Storage.Item.Get&name='+name)

        return self.render_template('Storage/export.html')
