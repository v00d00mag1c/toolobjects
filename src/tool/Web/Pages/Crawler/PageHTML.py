from App.Objects.Object import Object
from pydantic import Field
from Web.Pages.Assets.Favicon import Favicon
from Web.Pages.Assets.Meta import Meta
from Web.Pages.Assets.URL import URL
from typing import Any, Generator
from Web.Pages.Page import Page

from bs4.dammit import EncodingDetector
from bs4 import BeautifulSoup

class PageHTML(Object):
    bs: Any = Field()

    def get_favicons(self, orig_page: Page, take_default: bool = True) -> Generator[Favicon]:
        for icon in self.bs.select("link[rel*='icon']"):
            favicon = Favicon(sizes = getattr(icon, 'sizes', None))
            favicon.set_url(icon.get('href'), orig_page.relative_url)
            favicon.set_node(icon)

            yield favicon

        if take_default:
            yield Favicon(url = orig_page.base_url + '/favicon.ico')

    def get_meta(self, orig_page: Page) -> Generator[Meta]:
        for tag in self.bs.select("meta"):
            meta = Meta()

            for key, attr in tag.attrs.items():
                if key == 'class':
                    continue

                setattr(meta, key, attr)

            yield meta

    def get_media(self, orig_page: Page, tags: list[str]):
        pass

    def get_urls(self, orig_page: Page):
        for tag in self.bs.select("a"):
            url = URL()

            for key, attr in tag.attrs.items():
                if key == 'target':
                    url.target = attr
                elif key == 'href':
                    is_protocol = False
                    _parts = attr.split(':')
                    if len(_parts) > 2:
                        is_protocol = _parts[1] != '/'

                    if attr[0] == '#':
                        self.log('url {0}: probaly anchor'.format(attr))
                    elif attr[0] == '' or attr == None:
                        self.log('url {0}: empty url'.format(attr))
                    elif is_protocol:
                        self.log('url {0}: probaly protocol'.format(attr))
                        url.set_url(attr)
                    else:
                        url.set_url(attr, orig_page.base_url)
                elif key == 'download':
                    url.is_download = True

            yield url

    def get_links(self):
        pass

    def get_scripts(self):
        pass

    def prettify(self) -> str:
        return self.bs.prettify()

    @classmethod
    def from_html(cls, html: str):
        html_encoding = EncodingDetector.find_declared_encoding(html, is_html=True)
        _src = cls(bs = BeautifulSoup(html, 'html.parser', from_encoding = html_encoding))

        return _src
