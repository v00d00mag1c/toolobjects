from App.Objects.Object import Object
from pydantic import Field
from App.Objects.Displayment import Displayment

class String(Object):
    value: str = Field()

    @classmethod
    def asArgument(cls, val):
        if val == None:
            return None

        return str(val)

    @classmethod
    def getDisplayments(cls):
        class DisplayAsString(Displayment):
            role = ['str']

            def implementation(self, i):
                orig = i.get('orig')
                return str(orig.value)

        return [DisplayAsString()]
