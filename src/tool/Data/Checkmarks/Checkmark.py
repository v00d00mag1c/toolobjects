from App.Objects.Object import Object
from App.Objects.Displayments.StringDisplayment import StringDisplayment
from App.Objects.Act import Act
from App.Objects.Relations.LinkInsertion import LinkInsertion
from Data.String import String
from pydantic import Field

class Checkmark(Object):
    state: bool = Field(default = False)
    label: String | LinkInsertion = Field(default = None)

    @classmethod
    def _displayments(cls):
        class DisplayAsString(Act):
            def implementation(self, i):
                orig = i.get('orig')
                _mark = "[ ]"
                if orig.state:
                    _mark = "[x]"

                # TODO remove
                _i = orig.to_json()
                return _mark + " " + _i.get('label').get('value') + ' '

        return [
            StringDisplayment(
                role = ['str'],
                value = DisplayAsString
            )]
