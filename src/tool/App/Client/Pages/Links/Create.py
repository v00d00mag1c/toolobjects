from App.Client.Displayment import Displayment
from App.Storage.StorageUUID import StorageUUID
import aiohttp_jinja2

class Create(Displayment):
    for_object = 'App.DB.Link'

    async def render_as_page(self, request, context):
        query = request.rel_url.query
        link_object = query.get('item')
        item = StorageUUID.fromString(link_object)
        item = item.toPython()

        context.update({
            'item': item
        })

        if request.method == 'POST':
            _query = await request.post()
            _to_link = _query.get('with').split(',')
            _role = _query.get('role').split(',')

            for _item in _to_link:
                _item = StorageUUID.fromString(_item).toPython()
                item.link(_item, _role)

            return self.redirect('/?i=App.Objects.Object&uuids='+link_object)

        return aiohttp_jinja2.render_template('Links/create.html', request, context)
