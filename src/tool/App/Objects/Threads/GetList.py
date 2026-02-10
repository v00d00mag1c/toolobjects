from App.Objects.Act import Act
from App.Objects.Responses.ObjectsList import ObjectsList
from App import app

class GetList(Act):
    def _implementation(self, i):
        _list = ObjectsList(items = [], unsaveable=  True)

        for item in app.ThreadsList.getAll():
            _list.append(item)

        return _list
