from App.Objects.Object import Object
from pydantic import Field
from App import app

class Item(Object):
    url: str = Field(default = None)
    name: str = Field(default = None)
    category_name: str = Field()

    def get_name(self):
        return app.Locales.get(self.name)

    def get_url(self):
        return '?i=' + self.url
