from App.Objects.Object import Object
from pydantic import Field
from App.Objects.Displayments.StringDisplayment import StringDisplayment
from App.Objects.Act import Act

class String(Object):
    value: str = Field()

    @classmethod
    def asArgument(cls, val):
        if val == None:
            return None

        return str(val)

    @classmethod
    def _displayments(cls):
        class DisplayAsString(Act):
            def _implementation(self, i):
                orig = i.get('orig')
                return str(orig.value)

        return [StringDisplayment(
            role = ['str'],
            value = DisplayAsString
        )]
