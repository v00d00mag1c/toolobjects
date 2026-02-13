from App.Objects.Act import Act
from App.Objects.Object import Object
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Argument import Argument
from App.Objects.Arguments.Assertions.NotNone import NotNone
from Data.Types.JSON import JSON
from Data.Types.String import String
from App import app

class NewJSON(Act):

    # internal usage only

    @classmethod
    def _arguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
            Argument(
                name = 'item',
                orig = Object,
                assertions = [NotNone()]
            ),
            Argument(
                name = 'json',
                orig = JSON,
                assertions = [NotNone()]
            )
        ])

    async def _implementation(self, i):
        item = i.get('item')
        json = i.get('json')
        saved_via = json.get('obj').get('saved_via').get('object_name')
        get_obj = app.ObjectsList.getByName(saved_via)

        assert get_obj != None, 'wrong saved_via!'

        item.getDb().flush_new_json(json)
        item.save(do_flush_content = False)
