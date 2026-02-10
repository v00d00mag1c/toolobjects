from App.Objects.Act import Act
from App.Objects.Responses.ObjectsList import ObjectsList
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Argument import Argument
from App.Objects.Arguments.ListArgument import ListArgument
from App.Objects.Arguments.Assertions.NotNoneAssertion import NotNoneAssertion
from Data.String import String
from Data.Boolean import Boolean
from Web.Crawler.Webdrivers.Webdriver import Webdriver
from Web.Crawler.Crawler import Crawler
from Web.Pages.Page import Page

from App import app

class ByURL(Act):
    async def implementation(self, i):
        urls = i.get('url')
        webdriver = i.get('webdriver')

        crawler = Crawler(webdriver = webdriver)
        crawler.check_global_options()
        crawler.check_requirements()
        items = ObjectsList(items = [])

        await crawler.start_webdriver()

        for url in urls:
            page = Page()
            page.create_file(app.Storage.get('tmp'))

            await crawler.set_url(url)
            # crawler.set_cookies()

            if i.get('scroll_down') == True:
                await crawler.scroll_down()

            page.set_title(crawler.get_title())
            page.url = crawler.get_url().geturl()
            page.base_url = crawler.get_base_url()
            page.relative_url = crawler.get_relative_url()

            html = crawler.get_parsed_html()

            if i.get('download_favicon') == True:
                for ico in html.get_favicons():
                    await ico.download()

            page.html.write(html)

            items.append(page)

        return items

    @classmethod
    def _arguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
            ListArgument(
                name = 'url',
                orig = String,
                assertions = [NotNoneAssertion()]
            ),
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
                name = 'webdriver',
                orig = Webdriver,
                id_allow = True,
                assertions = [NotNoneAssertion()]
            )
        ])
