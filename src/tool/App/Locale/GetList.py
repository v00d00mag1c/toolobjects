from App.Objects.Act import Act
from App.Locale.Lang import Lang
from App.Objects.Responses.ObjectsList import ObjectsList
from App import app

class GetList(Act):
    def implementation(self, i):
        _list = ObjectsList(items = [], unsaveable = True)

        for item in app.Locales.getItems():
            _list.append(item)

        return _list
