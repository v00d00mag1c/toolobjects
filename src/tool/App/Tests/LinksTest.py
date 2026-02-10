from App.Objects.Test import Test
from Data.Text.Text import Text
from App.Objects.Relations.Link import Link

class LinksTest(Test):
    async def implementation(self, i):
        txt = Text(value='abcdefg')
        txt2 = Text(value='hijklmnopqrs')

        txt.addLink(Link(
            item = txt2,
            role = ['common'],
        ))
        self.log_raw(txt.model_dump_json(indent=4))
