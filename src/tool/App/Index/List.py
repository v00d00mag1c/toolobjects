from App.Objects.Object import Object
from Data.Increment import Increment
from Data.DictList import DictList

class List(Object):
    id: Increment = None
    items: DictList = None
    calls: list = []

    def constructor(self):
        self.id = Increment()
        self.items = DictList(items = [])

    def load(self):
        self.log("Loading plugins list: ")
