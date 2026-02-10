from App.Objects.Object import Object
from Web.Pages.Page import Page
from urllib.parse import urlparse
from pydantic import Field

class Original(Object):
    url_override: str = Field(default = None)

    async def process_page(self, page: Page, i: dict):
        html = page.get_parsed_html()
