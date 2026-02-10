from App.Objects.Act import Act
from Web.Pages.Downloader.Downloader import Downloader
from App.Objects.Responses.ObjectsList import ObjectsList
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.ListArgument import ListArgument
from App.Objects.Arguments.Assertions.NotNone import NotNone
from Data.Types.String import String
from Web.Pages.Page import Page

class ByURL(Act):
    async def _implementation(self, i):
        urls = i.get('url')
        webdriver = i.get('webdriver')
        items = ObjectsList(items = [])

        downloader = Downloader(webdriver = webdriver)
        downloader.check_global_options()
        downloader.check_requirements()
        await downloader.start_webdriver(i)

        it = 1

        for url in urls:
            self.log('{0}st URL'.format(it))
            new_page = Page()
            new_page.set_downloader(downloader)
            await new_page.from_url(url)

            items.append(new_page)

            it += 1

        return items

    @classmethod
    def _arguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
            ListArgument(
                name = 'url',
                orig = String,
                assertions = [NotNone()]
            )
        ]).join_class(Downloader)
