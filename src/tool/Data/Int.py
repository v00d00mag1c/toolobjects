from App.Objects.Object import Object
from App.Objects.Displayments.StringDisplayment import StringDisplayment
from App.Objects.Act import Act

class Int(Object):
    # It should be named "Integer"
    value: int = None

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

    @classmethod
    def asArgument(cls, val):
        if val == None:
            return None

        return int(val)
