from App.Objects.Act import Act
from App import app
from App.DB.Query.Condition import Condition
from App.DB.Query.Values.Value import Value
from App.Objects.Responses.ObjectsList import ObjectsList
from Web.Crawler.Webdrivers.Webdriver import Webdriver

class Get(Act):
    def _implementation(self, i):
        _query = app.Storage.get('bin').adapter.getQuery()
        _query.addCondition(Condition(
            val1 = Value(
                column = 'content',
                json_fields = ['platform'],
            ),
            operator = '!=',
            val2 = Value(
                value = None
            ),
        ))

        _items = ObjectsList(items = [], unsaveable = True)
        for item in _query.getAll():
            _items.append(item.toPython())

        return _items
