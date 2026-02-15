from App.Client.Displayment import Displayment
from App import app
import aiohttp_jinja2

class Index(Displayment):
    for_object = 'App.Client.Client'

    async def render_as_page(self, args = {}):
        self.context.update({
            'is_index': True,
            'namespaces': app.ObjectsList.namespaces,
            'storages': app.Storage.getAll()
        })

        try:
            menu_collections = self.getOption('web.index.collection')
            if menu_collections:
                generators = list()
                for item in menu_collections:
                    _item = item.toPython()
                    if _item == None:
                        continue

                    for link in _item.getLinked():
                        generators.append(link)

                self.context.update({
                    'generators': generators
                })
        except Exception as e:
            self.log_error(e)

        return self.render_template('index.html')

    async def render_as_error(self, request, context):
        return aiohttp_jinja2.render_template('error.html', request, context)
