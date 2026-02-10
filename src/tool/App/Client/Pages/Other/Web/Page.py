from App.Client.Displayment import Displayment
from Web.Pages.Crawler.PageHTML import PageHTML
from App.Storage.StorageUUID import StorageUUID
from Web.Pages.Assets.Asset import Asset

class Page(Displayment):
    for_object = 'Web.Pages.Page'
    prefer_object_displayment = 'page'

    async def render_as_page(self, args = {}):
        query = self.request.rel_url.query
        act = query.get('act')
        item = args.get('item')
        if item == None:
            item = StorageUUID.fromString(query.get('item')).toPython()

        assert item != None, 'not found page'

        match (act):
            case 'url':
                url = query.get('url')
                self.context.update({
                    'item': item,
                    'url': Asset.get_decoded_url(url),
                    'back': '/?i=App.Objects.Object&uuids={0}&act=display&as=Web.Pages.Page'.format(item.getDbIds())
                })

                return self.render_template('Other/Web/page_url.html')

        hide_banner = query.get('hide_banner') == '1'
        html_path = item._get('html').get_main()

        html = html_path.read_text(encoding = item.html.encoding)

        html = PageHTML.from_html(html)
        html.make_correct_links(item)
        head_html = html.move_head()

        self.context.update({
            'item': item,
            'head_html': head_html,
            'html': html.prettify(),
            'hide_banner': hide_banner
        })

        return self.render_template('Other/Web/page.html')
