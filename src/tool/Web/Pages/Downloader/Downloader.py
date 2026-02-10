from App.Objects.Object import Object
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Argument import Argument
from App.Objects.Arguments.ListArgument import ListArgument
from App.Objects.Arguments.Assertions.NotNone import NotNone
from Data.Types.Boolean import Boolean
from Data.Types.String import String
from Web.Pages.Page import Page
from Web.Pages.Crawler.Webdrivers.Webdriver import Webdriver
from pydantic import Field
from Data.Types.String import String
from Data.Types.Int import Int
from Data.Types.Float import Float
from App import app

class Downloader(Object):
    webdriver: Webdriver = Field(default = None)

    async def start_webdriver(self, i):
        await self.webdriver.start(i)

    @classmethod
    def _settings(cls):
        return [
            Argument(
                name = 'web.crawler.user_agent',
                default = None,
                orig = String
            ),
            Argument(
                name = 'web.crawler.scroll_cycles',
                default = None,
                orig = Int
            ),
            Argument(
                name = 'web.crawler.scroll_timeout',
                default = 1,
                orig = Float
            ),
            Argument(
                name = 'web.crawler.implicitly_wait',
                default = 5,
                orig = Int
            ),
        ]
        '''ListArgument(
            name = 'web.crawler.cookies',
            default = [],
            orig = Cookies
        ),'''

    async def _create_page(self, crawler, i):
        html = crawler.get_parsed_html()

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

        return page

    @classmethod
    def getArguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
            Argument(
                name = 'scroll_down',
                orig = Boolean,
                default = True
            ),
            Argument(
                name = 'webdriver.sizes',
                default = '1920,1200',
                orig = String
            ),
            Argument(
                name = 'download.favicon',
                orig = Boolean,
                default = True
            ),
            Argument(
                name = 'data.meta',
                orig = Boolean,
                default = True
            ),
            Argument(
                name = 'download.media',
                orig = Boolean,
                default = True
            ),
            ListArgument(
                name = 'download.media.selectors',
                orig = String,
                default = True
            ),
            Argument(
                name = 'data.save_urls',
                orig = Boolean,
                default = True
            ),
            Argument(
                name = 'webdriver',
                orig = Webdriver,
                by_id = True,
                assertions = [NotNone()]
            ),
            Argument(
                name = 'webdriver.headless',
                orig = Boolean,
            ),
            ListArgument(
                name = 'webdriver.args',
                orig = String,
            )
        ])
