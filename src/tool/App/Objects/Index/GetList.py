from App.Objects.Act import Act
from App.Objects.Responses.ObjectsList import ObjectsList
from App import app

class GetList(Act):
    def implementation(self, i):
        _items = ObjectsList(unsaveable = True)
        for item in app.ObjectsList.getItems().toList():
            try:
                item.to_json()
                _items.append(item)
            except Exception as e:
                self.log_error(e)

        return _items
