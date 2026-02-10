from App.Objects.Object import Object

class Increment(Object):
    _id: int = 0

    def __init__(self):
        self._id = 0

    def increment(self):
        self._id += 1

    def getIndex(self):
        self.increment()

        return self.getCount()

    def getCount(self):
        return self._id

    def null(self):
        self._id = 0
