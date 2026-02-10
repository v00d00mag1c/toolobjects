from App.Objects.Act import Act
from App.Objects.Object import Object
from Web.Pages.Downloader.Downloader import Downloader
from App.Objects.Responses.ObjectsList import ObjectsList
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.ListArgument import ListArgument
from App.Objects.Arguments.Argument import Argument
from App.Objects.Arguments.Assertions.NotNone import NotNone
from Web.Pages.Get import Get
from Web.Pages.Crawler.Original import Original
from Data.Types.String import String
from Web.Pages.Page import Page
from App import app

class ByURL(Act):
    async def _implementation(self, i):
        urls = i.get('url')
        webdriver = i.get('webdriver')
        do_crawl = i.get('crawl')
        crawler = i.get('mode')
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
            if do_crawl:
                new_page.set_crawler(crawler)

            new_page.create_file(app.Storage.get('tmp'))

            await new_page.from_url(url)
            # ???
            await new_page._crawler.crawl(new_page, i)

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
            ),
            Argument(
                name = 'mode',
                orig = Object,
                assertions = [NotNone()]
            ),
        ]).join_class(Downloader).join_class(Get).join_class(Original)
