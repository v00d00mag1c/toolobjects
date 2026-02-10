from App.Objects.Test import Test
from Data.Text import Text
from Data.JSON import JSON

class ContentLinksTest(Test):
    async def implementation(self, i):
        _text = Text(text = '7777')
        _another_text = Text(text = '66666')
        _got_link = _text.link(_another_text)
        #_another_text.link(_text) pydantic protects us from recursion

        _text.text = _got_link.toInsert(["text"])

        _json = JSON(data = _text.to_json())
        _json_no_links = JSON(data = _text.to_json(convert_links = False))

        self.log_error('with removed links:')
        self.log_raw(_json.dump(indent = 4))
        self.log_error('with links:')
        self.log_raw(_json_no_links.dump(indent = 4))
