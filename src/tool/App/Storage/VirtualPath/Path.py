from App.Objects.Object import Object
from App.Responses.ObjectsList import ObjectsList
from typing import ClassVar
from pydantic import Field
from App import app

class Path(Object):
    '''
    allows to view db items hierarchically as in file manager
    '''

    root: str = Field()
    parts: list[str | int] = Field(default = [])
    divider: str = '/'
    connection_divider: ClassVar[str] = ':/'

    @staticmethod
    def fromStr(str: str):
        _itms = str.split(Path.connection_divider)
        _res = Path(root = _itms[0])
        _res.setParts(_itms[1])

        return _res

    def setParts(self, items: str | list):
        if type(items) == str:
            if len(items) == 0:
                return

            for item in items.split(self.divider):
                self.parts.append(item)
        else:
            self.parts = items

    def getRoot(self):
        _root_parts = self.root.split(':')
        match(_root_parts[0]):
            case _:
                return app.Storage.get(_root_parts[1])

    def getContent(self) -> ObjectsList | Object:
        root = self.getRoot()
        db = root.adapter
        cursor = None
        res = None

        res = ObjectsList()

        if len(self.parts) == 0:
            for item in db.ObjectUnit.getQuery().limit(10):
                res.append(item.getObject())
        else:
            end_is_linked = False
            for part in self.parts:
                # it means that we want to get linked of this item
                if len(part) == 0:
                    end_is_linked = True
                    cursor = cursor.getLinkedItems()

                    continue

                _cursor = db.ObjectUnit.getById(int(part))
                assert _cursor != None, f"item with id {int(part)} not found"

                if cursor != None:
                    assert cursor.isLinked(_cursor), 'items are not linked'

                cursor = _cursor.getObject()

            if end_is_linked == False:
                res.supposed_to_be_single = True
                res.append(cursor)
            else:
                for item in cursor:
                    res.append(item)

        return res
