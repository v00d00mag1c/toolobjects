from App.Objects.Object import Object
from App.Objects.Displayment import Displayment
from Data.Checkmarks.Checkmark import Checkmark
from App.Objects.Act import Act
from typing import Generator

class List(Object):
    def getCheckmarks(self) -> Generator[Checkmark]:
        for link in self.getLinked():
            item = link.item
            if item.isInstance(Checkmark):
                yield item

    @classmethod
    def getDisplayments(cls):
        class DisplayAsString(Act):
            role = ['str']

            def implementation(self, i):
                orig = i.get('orig')
                _out = f"Checkmarks list \"{str(orig.obj.any_name)}\""
                _out += "\n"

                for checkmark in orig.getCheckmarks():
                    _out += checkmark.displayAsString()

                _out += "\n"

                return _out

        return [
            Displayment( 
                role = ['str'],
                value = DisplayAsString
            )
        ]
