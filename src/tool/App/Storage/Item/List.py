from App.Objects.Act import Act
from App.Objects.Responses.ObjectsList import ObjectsList
from App import app

class List(Act):
    def _implementation(self, i):
        _list = ObjectsList(items = [], unsaveable = True)

        for item in app.Storage.getAll():
            _list.append(item)

        return _list
