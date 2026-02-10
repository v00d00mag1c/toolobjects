from App.Objects.Object import Object
from App.Objects.Displayments.StringDisplayment import StringDisplayment
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
    def _displayments(cls):
        class DisplayAsString(Act):
            def implementation(self, i):
                orig = i.get('orig')
                _out = f"Checkmarks list \"{str(orig.obj.any_name)}\""
                _out += "\n"

                for checkmark in orig.getCheckmarks():
                    _out += checkmark.displayAsString()

                _out += "\n"

                return _out

        return [
            StringDisplayment( 
                role = ['str'],
                value = DisplayAsString
            )
        ]
