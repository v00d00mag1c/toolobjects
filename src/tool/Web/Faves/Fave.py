from App.Objects.Object import Object
from Web.URL import URL
from Web.Pages.Page import Page
from pydantic import Field

class Fave(Object):
    page: Page = Field()
    title: str = Field(default = None)
