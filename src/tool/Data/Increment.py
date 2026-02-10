from App.Objects.Object import Object
from pydantic import Field

class Increment(Object):
    value: int = Field(default = None)

    def init_hook(self):
        if self.value == None:
            self.value = 0

    def increment(self):
        self.value += 1

    def getIndex(self):
        self.increment()

        return self.getCount()

    def getCount(self):
        return self.value

    def move(self, new: int):
        self.value = new

    def null(self):
        self.value = 0
