from App.Objects.Object import Object
from pydantic import Field
from typing import Optional
from Web.Pages.Crawler.PageHTML import PageHTML

class EntryContent(Object):
    type: Optional[str] = Field(default = 'html')
    content: str = Field(default = '')

    async def update(self):
        html = PageHTML.from_html(self.content)
        #html.clear_js()

        # TODO download images
        #for image in html.bs.select('img'):


        self.content = html.prettify()

    def get_html(self):
        return self.content
