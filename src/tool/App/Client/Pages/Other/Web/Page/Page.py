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

        if act in ['url', 'options']:
            self.context.update({
                'item': item,
                'back': '/?i=App.Objects.Object&uuids={0}&act=display&as=Web.Pages.Page'.format(item.getDbIds()),
            })

        match (act):
            case 'url':
                url = query.get('url')
                new_url = Asset.get_decoded_url(url)
                redirect_url = item.relative_url + new_url

                if new_url.startswith(item.relative_url) or new_url.startswith('http'):
                    redirect_url = new_url

                self.context.update({
                    'url': new_url,
                    'redirect_url': redirect_url
                })
                return self.render_template('Other/Web/Page/page_url.html')
            case 'options':
                return self.render_template('Other/Web/Page/options.html')

        encoding = item.html.encoding
        encoding = 'utf-8'
        if query.get('encoding') != None:
            encoding = query.get('encoding')

        hide_banner = query.get('hide_banner') == 'on'
        disable_js = query.get('disable_js') == 'on'
        disable_css = query.get('disable_css') == 'on'
        disable_iframes = query.get('disable_iframes', 'on') == 'on'
        html_path = item._get('html').get_main()

        html = html_path.read_text(encoding = encoding)

        html = PageHTML.from_html(html)
        if disable_js:
            html.clear_js()
        if disable_css:
            html.remove_css()
        if disable_iframes:
            html.remove_iframes()

        html.make_correct_links(item)
        head_html = html.move_head()

        self.context.update({
            'item': item,
            'head_html': head_html,
            'html': html.prettify(),
            'hide_banner': hide_banner,
            'options_url': '/?i=Web.Pages.Page&item={0}&act=options'.format(item.getDbIds())
        })

        return self.render_template('Other/Web/Page/page.html')
