from App.Objects.Act import Act
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Argument import Argument
from App.Objects.Arguments.ListArgument import ListArgument
from Data.Boolean import Boolean
from Data.String import String
from Web.Crawler.Webdrivers.Webdriver import Webdriver
from App.Objects.Arguments.Assertions.NotNone import NotNone
from Web.Pages.Page import Page
from App import app

class Downloader(Act):
    @classmethod
    def _arguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
            Argument(
                name = 'scroll_down',
                orig = Boolean,
                default = True
            ),
            Argument(
                name = 'download_favicon',
                orig = Boolean,
                default = True
            ),
            Argument(
                name = 'parse_meta',
                orig = Boolean,
                default = True
            ),
            Argument(
                name = 'download_media',
                orig = Boolean,
                default = True
            ),
            ListArgument(
                name = 'download_media_with_tags',
                orig = String,
                default = True
            ),
            Argument(
                name = 'find_urls',
                orig = Boolean,
                default = True
            ),
            Argument(
                name = 'take_screenshot',
                orig = Boolean,
                default = True
            ),
            Argument(
                name = 'remove_scripts',
                orig = Boolean,
                default = True
            ),
            Argument(
                name = 'remove_styles',
                orig = Boolean,
                default = True
            ),
            Argument(
                name = 'webdriver',
                orig = Webdriver,
                by_id = True,
                assertions = [NotNone()]
            )
        ])

    async def _create_page(self, crawler, i):
        page = Page()
        page.create_file(app.Storage.get('tmp'))

        # crawler.set_cookies()

        if i.get('scroll_down') == True:
            await crawler.scroll_down()

        page.set_title(crawler.get_title())
        page.url = crawler.get_url().geturl()
        page.base_url = crawler.get_base_url()
        page.relative_url = crawler.get_relative_url()

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
