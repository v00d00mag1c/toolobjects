from App.Objects.Object import Object
from App.Objects.Displayment import Displayment
from App.Objects.Act import Act

class Int(Object):
    value: int = None

    @classmethod
    def getDisplayments(cls):
        class DisplayAsString(Act):
            role = ['str']

            def implementation(self, i):
                orig = i.get('orig')
                return str(orig.value)

        return [Displayment(
            role = ['str'],
            value = DisplayAsString
        )]

    @classmethod
    def asArgument(cls, val):
        if val == None:
            return None

        return int(val)
