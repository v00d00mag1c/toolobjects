from App.Tests.Test import Test
from Data.Text import Text
from App.Objects.Link import Link, LinkTypeEnum

class LinksTest(Test):
    async def implementation(self, i):
        txt = Text(text='abcdefg')
        txt2 = Text(text='hijklmnopqrs')

        txt.addLink(Link(
            item = txt2,
            common = True,
            link_type = LinkTypeEnum.EXTERNAL.value
        ))
        print(txt)
