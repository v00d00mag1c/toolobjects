from App.Client.Displayment import Displayment
from App.Storage.Movement.Save import Save
from App import app

class Copy(Displayment):
    for_object = 'App.Storage.Movement.Save'

    async def render_as_page(self, args = {}):
        query = self.request.rel_url.query
        items = query.get('items')

        self.context.update({
            'items': items,
            'ref': query.get('ref')
        })

        if self.is_post():
            data = await self.request.post()
            uuids = data.get('uuids')
            to = app.Storage.get(data.get('to'))

            if to != None:
                await Save().execute({
                    'items': uuids,
                    'storage': [to],
                    'just_copy': True
                })

                return self.redirect('/?i=App.Storage.Item.Get&name='+to.name)
        else:
            self.throw_message(app.Locale.get('client.storage.move.errors.no_storage'))

        return self.render_template('Actions/copy.html')
