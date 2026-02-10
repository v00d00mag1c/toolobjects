from Data.JSON import JSON
from App import app

class ObjectAdapter():
    '''
    Transition class between App.Objects.Object and SQL

    must contain uuid and content
    '''

    def search(self):
        pass

    def save(self):
        pass

    def getObject(self):
        _content = JSON().fromText(self.content)
        _object_name = _content.data.get('saved_via').get('object_name')
        _class = app.ObjectsList.getByName(_object_name).getModule()

        return _class.model_validate(_content.data, strict = False)
