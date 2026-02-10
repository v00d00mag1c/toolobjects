from App.Objects.Object import Object
from App.Objects.Displayment import Displayment
from App.Objects.Submodule import Submodule

class Number(Object):
    number: int | float = None

    class DisplayAsString(Displayment):
        role = ['str']

        def implementation(self, i):
            _object = i.get('object')
            return _object.number

    @classmethod
    def getSubmodules(cls):
        return [
            Submodule(
                item = cls.DisplayAsString,
                role = ['displayment']
            )
        ]
