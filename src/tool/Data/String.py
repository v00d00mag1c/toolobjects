from App.Objects.Object import Object
from pydantic import Field
from App.Objects.Displayment import Displayment
from App.Objects.Act import Act

class String(Object):
    value: str = Field()

    @classmethod
    def asArgument(cls, val):
        if val == None:
            return None

        return str(val)

    @classmethod
    def getDisplayments(cls):
        class DisplayAsString(Act):
            def implementation(self, i):
                orig = i.get('orig')
                return str(orig.value)

        return [Displayment(
            role = ['str'],
            value = DisplayAsString
        )]
