from App.Objects.Object import Object
from App.Objects.Responses.ObjectsList import ObjectsList
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
    def from_str(str: str):
        _root_and_other = str.split(Path.connection_divider)
        _path = Path(root = _root_and_other[0])

        for item in _root_and_other[1].split(_path.divider):
            _path.parts.append(item)

        return _path

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
            for item in db.ObjectAdapter.getQuery().limit(10):
                res.append(item.toPython())
        else:
            end_is_linked = False
            for part in self.parts:
                # it means that we want to get linked of this item
                if len(part) == 0:
                    end_is_linked = True
                    cursor = cursor.getLinkedItems()

                    continue

                _cursor = db.ObjectAdapter.getById(int(part))
                assert _cursor != None, f"item with id {int(part)} not found"

                if cursor != None:
                    assert cursor.isLinked(_cursor), 'items are not linked'

                cursor = _cursor.toPython()

            if end_is_linked == False:
                res.supposed_to_be_single = True
                res.append(cursor)
            else:
                for item in cursor:
                    res.append(item)

        return res
