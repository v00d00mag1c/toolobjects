from App.Objects.Object import Object
from App.Client.Menu.Item import Item
from typing import ClassVar
from abc import abstractmethod
from Data.Types.JSON import JSON
import aiohttp

class Displayment(Object):
    '''
    Representation of object in client (template render of each object)
    '''

    for_object: ClassVar[str] = ''
    self_name = 'ClientDisplayment'

    @abstractmethod
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
