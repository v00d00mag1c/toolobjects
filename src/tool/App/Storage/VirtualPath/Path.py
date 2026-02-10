from App.Objects.Object import Object
from typing import ClassVar
from pydantic import Field
from App import app

class Path(Object):
    root: str = Field()
    parts: list[str | int] = Field(default = [])
    has_parts: bool = Field(default = True)
    divider: str = '/'
    connection_divider: ClassVar[str] = ':/'

    @classmethod
    def asArgument(cls, val):
        if val == None:
            return None

        if isinstance(val, Path):
            return val

        return Path.from_str(val)

    @staticmethod
    def from_str(str: str):
        _root_and_other = str.split(Path.connection_divider)
        _path = Path(root = _root_and_other[0])

        # If nothing, even the root was not passed, its supposed that will show list of storage items like "This PC" on win or like in kde dolphin
        _paths = _root_and_other[1]
        if len(_root_and_other) > 1:
            if len(_paths) > 0:
                for item in _paths[1:].split(_path.divider):
                    _path.parts.append(item)
        else:
            _path.has_parts = False

        return _path

    def join(self, parts = None):
        if parts == None:
            parts = self.parts

        return self.root + Path.connection_divider + '/'.join(parts)

    def prev(self):
        if len(self.parts) == 0:
            return ''

        return self.join(self.parts[-1:])

    def get_root(self):
        _root = self.root

        return app.Storage.get(_root)

    def to_args(self) -> dict:
        root_name = self.root
        root = self.get_root()
        cursor = None

        if len(self.parts) == 0:
            _root_uuid = root.root_uuid
            if _root_uuid != None:
                _item = ''
                if root_name in _root_uuid:
                    _item = _root_uuid
                else:
                    _item = root_name + '_' + _root_uuid

                return self.get_dict({
                    'linked_to': _item
                })
            else:
                self.log('root_uuid is None, so returning everything')

                return {}

        for part in self.parts:
            if len(part) == 0:
                return self.get_dict({
                    'linked_to': root_name + '_' + str(cursor)
                })

            cursor = part

        return self.get_dict({
            'uuids': [root_name + '_' + str(cursor)]
        })

    # ???
    def get_dict(self, new: dict):
        return new
