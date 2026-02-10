from App.Objects.Test import Test
from App.Console.ConsoleView import ConsoleView

class UpdateTest(Test):
    async def implementation(self, i):
        _view = ConsoleView()
        await _view.byString("-i Media.RSS.GetFeed -url https://feeds.bbci.co.uk/news/world/rss.xml -force_flush 1 -save_to tmp")
        await _view.byString("-i App.DB.Search -storage tmp")
        # not so flexible
        await _view.byString("-i App.Objects.Operations.ExecuteById -item content_7409176851433783296 -is_update 1")

        return None
