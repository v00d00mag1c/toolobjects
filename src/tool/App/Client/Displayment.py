from App.Objects.Object import Object
from App.Client.Menu.Item import Item
from typing import ClassVar, Any
from abc import abstractmethod
from App.Storage.StorageUUID import StorageUUID
from Data.Types.JSON import JSON
import aiohttp_jinja2
import aiohttp

class Displayment(Object):
    '''
    Representation of object in client (template render of each object)
    '''

    for_object: ClassVar[str] = ''
    request: Any = None
    context: Any = {}
    auth: Any = None
    self_name = 'ClientDisplayment'

    def render_as_page(self, request, context):
        ...

    @classmethod
    def get_menu(self) -> Item:
        return None

    def return_json(self, val):
        return aiohttp.web.Response(
            text = JSON(data = val).dump(4),
            content_type = 'application/json'
        )

    def render_template(self, template: str):
        return aiohttp_jinja2.render_template(template, self.request, self.context)

    def render_string(self, template: str):
        return aiohttp_jinja2.render_string(template, self.request, self.context)

    def get_objs(self, uuids):
        objs = list()
        for id in uuids:
            objs.append(StorageUUID.fromString(id).toPython())

        return objs

    def redirect(self, url: str):
        return aiohttp.web.HTTPFound(url)
