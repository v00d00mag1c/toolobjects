from App.Client.Displayment import Displayment
from Media.Files.FileSize import FileSize
from App import app
from Data.Types.JSON import JSON
import aiohttp_jinja2
import aiohttp

class Get(Displayment):
    for_object = 'App.Storage.Item.Get'

    async def render_as_page(self, request, context):
        query = request.rel_url.query
        item = app.Storage.get(query.get('name'))

        assert item != None, 'not found namespace'

        if query.get('get_settings') == '1':
            return self.return_json(item.db)

        if request.method == 'POST' and query.get('clear') == '1':
            item.storage_adapter.clear()

        context.update({
            'item': item,
            'FileSize': FileSize,
        })

        if query.get('calculate_db') == '1':
            context.update({
                'rows_count': item.adapter.get_rows_count(),
                'links_count': item.adapter.get_links_count(),
            })

        if query.get('calculate') == '1':
            context.update({
                'storage_size': item.storage_adapter.get_size()
            })

        return aiohttp_jinja2.render_template('Storage/item.html', request, context)
