from Web.Pages.Download.Downloader import Downloader
from App.Objects.Responses.ObjectsList import ObjectsList
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.ListArgument import ListArgument
from App.Objects.Arguments.Assertions.NotNoneAssertion import NotNoneAssertion
from Data.String import String
from Web.Crawler.Crawler import Crawler

class ByURL(Downloader):
    async def implementation(self, i):
        urls = i.get('url')
        webdriver = i.get('webdriver')

        crawler = Crawler(webdriver = webdriver)
        crawler.check_global_options()
        crawler.check_requirements()

        items = ObjectsList(items = [])

        await crawler.start_webdriver()

        for url in urls:
            await crawler.set_url(url)

            items.append(await self._create_page(crawler, i))

        return items

    @classmethod
    def _arguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
            ListArgument(
                name = 'url',
                orig = String,
                assertions = [NotNoneAssertion()]
            )
        ])
