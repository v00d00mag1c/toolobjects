from App.Client.Displayment import Displayment
from bs4 import BeautifulSoup
import aiohttp

class Page(Displayment):
    for_object = 'Web.Pages.Page'
    prefer_object_displayment = 'page'

    async def render_as_page(self):
        item = self.context.get('item')
        html_path = item._get('html').get_main()
        html = html_path.read_text()

        self.context.update({
            'item': item,
            'html': html
        })

        return self.render_template('Other/Web/page.html')
