from App.Client.Displayment import Displayment
from Web.Pages.Crawler.PageHTML import PageHTML
from App.Storage.StorageUUID import StorageUUID
from Web.Pages.Assets.Asset import Asset

class Page(Displayment):
    for_object = 'Web.Pages.Page'
    prefer_object_displayment = 'page'

    async def render_as_page(self, args = {}):
        query = dict(self.request.rel_url.query)

        act = query.get('web_act', 'switch')
        item = args.get('item')
        if item == None:
            item = StorageUUID.fromString(query.get('item')).toPython()

        assert item != None, 'not found page'

        self.context.update({
            'item': item,
            'back': '/?i=App.Objects.Object&uuids={0}'.format(item.getDbIds()),
        })

        if act == 'text_only':
            act = 'render_page'
            query['disable_js'] = 'on'
            query['disable_css'] = 'on'
            query['remove_inline_styles'] = 'on'
            query['disable_iframes'] = 'on'
            query['remove_selectors'] = 'nav, header, input'

        match (act):
            case 'meta':
                return self.render_template('Other/Web/Page/meta.html')
            case 'switch':
                thumbs = list(item.get_thumbnails())
                if len(thumbs) > 0:
                    self.context['thumb'] = thumbs[0].getItem()
                if len(thumbs) > 1:
                    self.context['fullsize_thumb_url'] = thumbs[1].getItem().get_url(True)

                self.context.update({
                    'url': '/?i=Web.Pages.Page&item={0}&web_act='.format(item.getDbIds())
                })
                return self.render_template('Other/Web/Page/page_switch.html')
            case 'hyperlinks' | 'media' | 'images':
                self.context.update({
                    'resources_act': act,
                    'ref': query.get('ref')
                })
                return self.render_template('Other/Web/Page/resources.html')
            case 'render_page':
                encoding = item.html.encoding
                encoding = 'utf-8'
                if query.get('encoding') != None:
                    encoding = query.get('encoding')

                hide_banner = query.get('hide_banner') == 'on'
                disable_js = query.get('disable_js') == 'on'
                disable_css = query.get('disable_css') == 'on'
                disable_iframes = query.get('disable_iframes', 'on') == 'on'
                remove_selectors = query.get('remove_selectors')
                html_path = item._get('html').get_main()

                html = html_path.read_text(encoding = encoding)

                html = PageHTML.from_html(html)
                if disable_js:
                    html.clear_js()
                if query.get('remove_inline_styles') == 'on':
                    html.remove_inline_css()
                if disable_css:
                    html.remove_css()
                if disable_iframes:
                    html.remove_iframes()
                if remove_selectors:
                    html.remove_selectors(remove_selectors)

                html.make_correct_links(item)
                head_html = html.move_head()

                self.context.update({
                    'item': item,
                    'head_html': head_html,
                    'html': html.prettify(),
                    'hide_banner': hide_banner,
                    'options_url': '/?i=Web.Pages.Page&item={0}&web_act=options'.format(item.getDbIds())
                })

                return self.render_template('Other/Web/Page/page.html')
            case 'url':
                url = query.get('url')
                new_url = Asset.get_decoded_url(url)
                redirect_url = item.get_relative_url(new_url)

                self.context.update({
                    'url': new_url,
                    'redirect_url': redirect_url
                })
                return self.render_template('Other/Web/Page/page_url.html')
            case 'options':
                return self.render_template('Other/Web/Page/options.html')
