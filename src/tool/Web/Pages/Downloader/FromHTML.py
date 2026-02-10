from App.Objects.Act import Act
from Web.Pages.Downloader.Downloader import Downloader
from App.Objects.Arguments.Argument import Argument
from App.Objects.Arguments.ListArgument import ListArgument
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Assertions.NotNone import NotNone
from Data.Types.String import String
from App.Objects.Responses.ObjectsList import ObjectsList
from Web.Pages.Page import Page
from Web.Pages.Get import Get
from Web.Pages.Crawler.Original import Original
from App import app

class FromHTML(Act):
    async def _implementation(self, i):
        webdriver = i.get('webdriver')
        do_crawl = i.get('crawl')
        crawler = i.get('mode')
        items = ObjectsList(items = [])

        downloader = Downloader(webdriver = webdriver)
        downloader.check_global_options()
        downloader.check_requirements()

        await downloader.start_webdriver(i)

        set_url = i.get('set_url')
        it = 1

        for item in i.get('html'):
            self.log('{0}st html'.format(it))

            new_page = Page()
            new_page.set_downloader(downloader)
            if do_crawl:
                new_page.set_crawler(crawler)

            new_page.create_file(app.Storage.get('tmp'))
            await new_page.from_html(set_url, item)
            await new_page._crawler.crawl(new_page, i)

            items.append(new_page)

            it += 1

        return items

    @classmethod
    def _arguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
            Argument(
                name = 'set_url',
                orig = String,
                assertions = [NotNone()]
            ),
            ListArgument(
                name = 'html',
                orig = String,
                allow_commas_fallback = False,
                assertions = [NotNone()]
            )
        ]).join_class(Downloader).join_class(Get).join_class(Original)
