from App.Objects.Extractor import Extractor
from App.Objects.Object import Object
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Assertions.NotNone import NotNone
from App.Objects.Arguments.Argument import Argument
from App.Objects.Arguments.ListArgument import ListArgument
from App.Objects.Responses.ObjectsList import ObjectsList
from Web.Pages.Crawler.Webdrivers.Webdriver import Webdriver
from Web.Pages.Downloader.Downloader import Downloader
from Media.Download import Download
from Web.URL import URL
from Data.Types.String import String
from Web.Pages.Page import Page

class FromPage(Extractor):
    @classmethod
    def _arguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
            Argument(
                name = 'object',
                orig = Object,
                assertions = [NotNone()]
            ),
            ListArgument(
                name = 'page_url',
                orig = URL,
                allow_comma_fallback = False,
                assertions = [NotNone()]
            ),
            ListArgument(
                name = 'selector',
                orig = String,
            ),
            ListArgument(
                name = 'allowed_selector',
                orig = String,
            ),
            Argument(
                name = 'webdriver',
                orig = Webdriver,
                by_id = True,
                assertions = [NotNone()]
            ),
        ],
        missing_args_inclusion=True).join_class(Downloader).join_class(Download, only = ['filename', 'download'])

    async def _implementation(self, i):
        webdriver = i.get('webdriver')
        selectors = i.get('selector')
        allowed_selectors = i.get('allowed_selector')
        object_type = i.get('object')
        for selector in object_type.get_page_js_selectors():
            selectors.append(selector)

        downloader = None

        if webdriver != None:
            downloader = Downloader(webdriver = webdriver)
            downloader.check_global_options()
            downloader.check_requirements()
            await downloader.start_webdriver(i)

        for page_url in i.get('page_url'):
            new_page = Page()
            new_page.set_downloader(downloader)
            await new_page.from_url(page_url)

            if i.get('web.crawler.scroll_down'):
                await new_page._page.scroll_down(i.get('web.crawler.scroll_down.cycles'))

            values = await new_page._page.get().evaluate("""
                (i) => {
                    selectors = i[0]
                    allowed_selectors = i[1]
                    const urls = [];
                    const elements = [];

                    if (selectors.length > 0) {
                        document.querySelectorAll(selectors).forEach(element => {
                            elements.push(element);
                        });                                    
                    }

                    """+object_type.get_page_js_function()+"""
                    """+object_type.get_page_js_return_function()+"""
                }
            """, [selectors, allowed_selectors])

            _vals = await object_type.convert_page_results(i, values)

            for _res_item in _vals.getItems():
                self.append(_res_item)
