from App.Client.Displayment import Displayment
from App.Storage.Clear import Clear as RealClear
from App.Storage.ClearTemp import ClearTemp

class Clear(Displayment):
    for_object = 'App.Storage.Clear'

    async def render_as_page(self, args = {}):
        query = self.request.rel_url.query
        act = query.get('act')
        storage_name = query.get('name')
        self.context.update({
            'storage_name': storage_name,
            'ref': query.get('ref'),
            'act': act
        })

        if self.is_post():
            data = await self.request.post()
            post_act = data.get('act')

            match (post_act):
                case 'storage':
                    await RealClear().execute({
                        'storage': storage_name
                    })
                case 'tmp':
                    await ClearTemp().execute({
                        'storage': storage_name
                    })
                case 'clear_all':
                    await self._execute('App.Storage.Item.Delete', {
                        'storage': storage_name
                    })
                    return self.redirect('/?i=App.Storage.Item.List')
                case 'unmount':
                    await self._execute('App.Storage.Item.Unmount', {
                        'name': storage_name,
                        'to_config': True
                    })
                    return self.redirect('/?i=App.Storage.Item.List')

            return self.redirect('/?i=App.Storage.Item.Get&name=' + storage_name)

        match (act):
            case 'clear_all':
                return self.render_template('Storage/clear.html')

        return self.render_template('Storage/clear.html')
