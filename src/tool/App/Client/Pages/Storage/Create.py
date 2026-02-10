from App.Client.Displayment import Displayment
from App.Storage.Item.Create import Create as RealCreate

class Create(Displayment):
    for_object = 'App.Storage.Item.Create'

    async def render_as_page(self, args = {}):
        if self.request.method == 'POST':
            data = await self.request.post()
            name = data.get('name')
            await RealCreate().execute({
                'name': name
            })

            return self.redirect('/?i=App.Storage.Item.Get&name='+name)

        return self.render_template('Storage/create.html')
