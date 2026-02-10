from App.Objects.Object import Object
from Web.Pages.Crawler.PageHTML import PageHTML
from Web.Pages.Page import Page
from urllib.parse import urlparse
from pydantic import Field
from App import app

class Original(Object):
    url_override: str = Field(default = None)

    async def process_page(self, page: Page, i: dict):
        await page.set_info()

        if i.get('scroll_down'):
            await page._page.scroll_down(i.get('web.crawler.scroll_down.cycles'), i.get('web.crawler.scroll_down.'))

        page.create_file(app.Storage.get('tmp'))
        # TODO rewrite to js scripts
        html = PageHTML.from_html(await page._page.get_html())

        if i.get('download_favicon') == True:
            for ico in html.get_favicons(page):
                self.log('downloading icon {0}'.format(ico.get_url()))

                await ico.download(page.html.get_assets_dir())
                ico.replace()

                page.favicons.append(ico)

        if i.get('parse_meta') == True:
            for meta in html.get_meta(page):
                _name = meta.get_name()
                if _name == None:
                    self.log('metatag {0} = {1}'.format(_name, meta.get_content()))
                else:
                    self.log('metatag: without name')

                page.meta_tags.append(meta)

        if i.get('download_media') == True:
            pass

        if i.get('find_urls') == True:
            for url in html.get_urls(page):
                self.log('find url {0}'.format(url.get_url()))

                page.page_links.append(url)

        page.html.write(html.prettify())
