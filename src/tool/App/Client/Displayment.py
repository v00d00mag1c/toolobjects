from App.Objects.Object import Object
from App.Client.Menu.Item import Item
from typing import ClassVar, Any, Literal
from abc import abstractmethod
from App.Storage.StorageUUID import StorageUUID
from Data.Types.JSON import JSON
from App import app
import aiohttp_jinja2
import aiohttp

class Displayment(Object):
    '''
    Representation of object in client (template render of each object)
    '''

    for_object: ClassVar[str | list[str]] = ''
    prefer_object_displayment: ClassVar[Literal['object', 'page']] = 'object'
    request: Any = None
    context: Any = {}
    auth: Any = None
    self_name = 'ClientDisplayment'

    # should return "render_template"
    async def render_as_page(self):
        ...

    # should return "render_string"
    async def render_as_list_item(self, args):
        ...

    async def render_as_object(self, item, args):
        ...

    async def render_as_collection(self, orig_items, args, orig_collection = None):
        ...

    @classmethod
    def get_for(cls, name: str):
        _item = app.app.view.displayments.get(name)
        if _item == None:
            return None

        return _item[0]

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

    def throw_message(self, message: str, message_type: str = None):
        self.context.update({
            'special_message': message
        })

    def get_objs(self, uuids):
        objs = list()
        for id in uuids:
            objs.append(StorageUUID.fromString(id).toPython())

        return objs

    def redirect(self, url: str):
        return aiohttp.web.HTTPFound(url)
