from Web.Pages.Download.Downloader import Downloader
from App.Objects.Arguments.Argument import Argument
from App.Objects.Arguments.ListArgument import ListArgument
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Assertions.NotNone import NotNone
from Data.String import String
from Web.Crawler.Crawler import Crawler
from App.Objects.Responses.ObjectsList import ObjectsList

class FromHTML(Downloader):
    async def _implementation(self, i):
        html = i.get('html')
        webdriver = i.get('webdriver')

        crawler = Crawler(webdriver = webdriver)
        crawler.check_global_options()
        crawler.check_requirements()
        items = ObjectsList(items = [])

        await crawler.start_webdriver()
        await crawler.set_url('about:blank')
        crawler.override_url(i.get('url'))
        crawler.webdriver._driver.execute_script(f"document.write(`{html}`);")

        _page = await self._create_page(crawler, i)

        items.append(_page)

        return items

    @classmethod
    def _arguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
            Argument(
                name = 'url',
                orig = String,
                assertions = [NotNone()]
            ),
            ListArgument(
                name = 'html',
                orig = String,
                assertions = [NotNone()]
            )
        ])
