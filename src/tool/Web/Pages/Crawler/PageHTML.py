from App.Objects.Object import Object
from pydantic import Field
from Web.Pages.Assets.Asset import Asset
from Web.Pages.Assets.Media import Media
from Web.Pages.Assets.Favicon import Favicon
from Web.Pages.Assets.Meta import Meta
from Web.Pages.Assets.Script import Script
from Web.Pages.Assets.Link import Link
from Web.Pages.Assets.URL import URL
from typing import Any, Generator
from Web.Pages.Page import Page

from bs4.dammit import EncodingDetector
from bs4 import BeautifulSoup
import re

class PageHTML(Object):
    bs: Any = None
    encoding: str = Field(default = None)

    def get_favicons(self, orig_page: Page, take_default: bool = True) -> Generator[Favicon]:
        for icon in self.bs.select("link[rel*='icon']"):
            favicon = Favicon(sizes = getattr(icon, 'sizes', None))
            favicon.set_url(orig_page.get_relative_url(icon.get('href')))
            favicon.set_node(icon)

            yield favicon

        if take_default:
            yield Favicon(url = orig_page.base_url + '/favicon.ico')

    def get_media(self, orig_page: Page) -> Generator[Favicon]:
        for tag in self.bs.select("img[src], video[src], audio[src]"):
            item = Media()
            item.tagName = tag.name
            item.set_url(orig_page.get_relative_url(tag.get('src')))
            item.set_node(tag)
            if tag.get('alt'):
                item.alt = tag.get('alt')

            yield item

    def get_meta(self, orig_page: Page) -> Generator[Meta]:
        for tag in self.bs.select("meta"):
            meta = Meta()
            meta.set_node(tag)

            for key, attr in tag.attrs.items():
                if key == 'class':
                    continue

                setattr(meta, key, attr)

            yield meta

    def get_links(self, orig_page: Page):
        for tag in self.bs.select("link"):
            item = Link()
            item.set_node(tag)

            for key, attr in tag.attrs.items():
                try:
                    if key == 'href':
                        item.set_url(orig_page.get_relative_url(attr))
                    else:
                        setattr(item, key, attr)
                except Exception as e:
                    self.log_error(e)

            yield item

    def get_downloadable_links(self, orig_page: Page):
        for item in self.get_links(orig_page):
            if item.should_download() == False:
                continue

            yield item

    def get_urls(self, orig_page: Page):
        for tag in self.bs.select("a"):
            label = tag.text

            url = URL()
            url.set_node(tag)
            if type(label) == str:
                url.label = label

            for key, attr in tag.attrs.items():
                try:
                    if key == 'target':
                        url.target = attr
                    elif key == 'href':
                        is_protocol = False
                        _parts = attr.split(':')
                        if len(_parts) > 2:
                            is_protocol = _parts[1] != '/'

                        if attr[0] == '#':
                            self.log('url {0}: anchor'.format(attr))
                        elif attr[0] == '' or attr == None:
                            self.log('url {0}: empty url'.format(attr))
                        elif is_protocol:
                            self.log('url {0}: probaly protocol'.format(attr))
                            url.set_protocol(attr)
                        else:
                            url.set_url(orig_page.get_relative_url(attr))
                    elif key == 'download':
                        url.is_download = True
                except Exception as e:
                    self.log_error(e)
                    continue

            yield url

    def get_scripts(self, orig_page: Page):
        for tag in self.bs.select("script"):
            item = Script()
            item.set_node(tag)

            if tag.get('src') != None:
                item.set_url(orig_page.get_relative_url(tag.get('src')))
            else:
                pass
                #for key, attr in tag.attrs.items():
                    #if key in ['rel', 'href']:
                    #    continue

                #    setattr(item, key, attr)

            yield item

    def move_head(self) -> str:
        head_html = ''
        for tag in ['title', 'meta', 'base', 'link']:
            for item in self.bs.select(tag):
                head_html += str(item)

                item.decompose()

        return head_html

    def remove_iframes(self):
        for tag in self.bs.select('iframe'):
            tag.decompose()

    def remove_selectors(self, selectors: list | str):
        if type(selectors) != list:
            selectors = [selectors]

        for selector in selectors:
            for tag in self.bs.select(selector):
                tag.decompose()

    def clear_js(self):
        # self.log('removing all js functions from tags')

        for tag in self.bs.select('script'):
            tag.decompose()

        for tag in self.bs.select('noscript'):
            tag.decompose()

        for tag in self.bs.select('*'):
            attrs_to_remove = []
            for attr in tag.attrs:
                if re.match(r'^on\w+', attr, re.IGNORECASE):
                    attrs_to_remove.append(attr)
                elif isinstance(tag[attr], str) and 'javascript:' in tag[attr].lower():
                    attrs_to_remove.append(attr)

            for attr in ['href', 'src', 'action']:
                if tag.has_attr(attr) and tag[attr] and 'javascript:' in str(tag[attr]).lower():
                    attrs_to_remove.append(tag[attr])

            tag.attrs = {key:value for key,value in tag.attrs.items()
                    if key not in attrs_to_remove}

    def remove_inline_css(self):
        for tag in self.bs.find_all(attrs={"style": True}):
            del tag['style']

    def remove_css(self):
        for tag in self.bs.select('style'):
            tag.decompose()

        for tag in self.bs.select('link[rel=\'stylesheet\']'):
            tag.decompose()

    def remove_integrity(self):
        for tag in self.bs.find_all(attrs={"integrity": True}):
            del tag['integrity']

    def make_correct_links(self, page):
        _s = page.html._get('file').get_storage_unit()

        for item in self.bs.select('link[href]'):
            if item.get('data-__to_orig_key') != None:
                continue

            _href = item.get('href')
            if _href:
                item['href'] = '{0}{1}'.format(page.relative_url, _href)

        # replacing assets
        for item in self.bs.select('[data-__to_orig]'):
            #_url = base64.urlsafe_b64encode(('assets/' + _file_url).encode()).decode()
            _url = item['data-__to_orig']
            _id = page.html.get_asset_by_url(_url)
            if _id == None:
                self.log_error('page {0}: element \"{1}\" is missing'.format(page.getDbIds(), _url))

                continue

            key = item['data-__to_orig_key']
            item[key] = '/storage/{0}/{1}/assets/{2}'.format(_s.getDbName(), _s.getDbId(), _id)

            # removing internal data attributes
            item.attrs = {key:value for key,value in item.attrs.items()
                    if key not in ['data-__to_orig_key', 'data-__to_orig']}

        for item in self.bs.select('meta[http-equiv]'):
            item.decompose()

        for item in self.bs.select('a[href]'):
            _href = item.get('href')
            if _href:
                if _href[0] == '#':
                    continue

                item['href'] = '/?i=Web.Pages.Page&item={0}&web_act=url&url={1}'.format(page.getDbIds(), Asset.encode_url(_href))

    def prettify(self) -> str:
        return self.bs.prettify()

    @classmethod
    def from_html(cls, html: str):
        _src = cls()
        _src.encoding = EncodingDetector.find_declared_encoding(html, is_html=True)
        #_src.log('detected encoding {0}'.format(_src.encoding))
        _src.bs = BeautifulSoup(html, 'html.parser')

        return _src
