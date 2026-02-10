from App.Client.Displayment import Displayment
from App.Storage.StorageUUID import StorageUUID
from App.DB.Link import Link as DoLink
import aiohttp_jinja2

class Create(Displayment):
    for_object = 'App.DB.Link'

    async def render_as_page(self):
        query = self.request.rel_url.query
        link_object = query.get('item')
        act = query.get('act', 'with')

        assert act in ['with', 'to']

        main_item = StorageUUID.fromString(link_object)
        main_item = main_item.toPython()

        self.context.update({
            'item': main_item,
            'act': act
        })

        if self.request.method == 'POST':
            _query = await self.request.post()
            _unlink = _query.get('unlink') == 'on'
            _to_link = _query.get('with').split(',')
            _role = _query.get('role').split(',')
            _act = 'unlink' if _unlink else 'link'
            items = list()

            for _item in _to_link:
                items.append(StorageUUID.fromString(_item).toPython())

            link_exec = DoLink()
            if act == 'with':
                await link_exec.execute({
                    'owner': main_item,
                    'items': items,
                    'act': _act,
                    'role': _role
                })

                return self.redirect('/?i=App.DB.Search&storage={0}&public=0&linked_to={1}'.format(main_item.getDbName(), main_item.getDbIds()))
            elif act == 'to':
                for item in items:
                    await link_exec.execute({
                        'owner': item,
                        'items': [main_item],
                        'act': _act,
                        'role': _role
                    })

                return self.redirect('/?i=App.Objects.Object&uuids='+link_object)

        return self.render_template('Links/create.html')
