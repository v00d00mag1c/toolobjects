from App.Objects.Act import Act
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Argument import Argument
from App.Objects.Arguments.ListArgument import ListArgument
from App.Objects.Arguments.Assertions.NotNoneAssertion import NotNoneAssertion
from Data.String import String
from Data.Boolean import Boolean
from Web.Crawler.Webdrivers.Webdriver import Webdriver
from Web.Crawler.Crawler import Crawler
from App import app

class ByURL(Act):
    async def implementation(self, i):
        urls = i.get('url')
        webdriver = i.get('webdriver')
        crawler = Crawler(webdriver = webdriver)
        crawler.check_requirements()

        app.Config.appendModule(Crawler)

        await crawler.start_webdriver()

        for url in urls:
            await crawler.get_url(url)

            if i.get('scroll_down') == True:
                await crawler.scroll_down()

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
                name = 'webdriver',
                orig = Webdriver,
                id_allow = True,
                assertions = [NotNoneAssertion()]
            )
        ])
