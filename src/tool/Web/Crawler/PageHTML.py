from App.Objects.Object import Object
from pydantic import Field
from Web.Pages.Assets.Favicon import Favicon
from typing import Any, Generator
from Web.Pages.Page import Page

class PageHTML(Object):
    bs: Any = Field()

    def get_favicons(self, orig_page: Page) -> Generator[Favicon]:
        for icon in self.bs.select("link[rel*='icon']"):
            favicon = Favicon(url = None, sizes = getattr(icon, 'sizes', None))
            favicon.set_url(getattr(icon, 'href', None), orig_page.relative_url)

            yield favicon
