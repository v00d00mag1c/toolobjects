from App.DB.ConnectionAdapter import ConnectionAdapter
from App.DB.Representation.ObjectAdapter import ObjectAdapter
from App.DB.Representation.LinkAdapter import LinkAdapter
from pydantic import Field
from App.Objects.Object import Object
from typing import Generator, Any
from App.Objects.Relations.Link import Link as CommonLink
from App.Objects.Relations.LinkData import LinkData
from App.Objects.Misc.UnknownObject import UnknownObject
from pathlib import Path
from App.DB.Query.Condition import Condition
from App.DB.Query.Values.Value import Value
from App.DB.Query.Sort import Sort
from App.DB.Query.Query import Query
from App.DB.Query.Operator import Operator
import json

class ObjectsList(ConnectionAdapter):
    '''
    json-file storage. its slow and not recommended to use
    '''

    protocol_name = 'objects_list'
    file: str = Field(default = None)
    indent: int = Field(default = None)

    data: dict = Field(default = None, repr = False)
    _stream: Any = None

    def _init_models(self_adapter):
        class QueryAdapter(Query):
            _model: Any = None
            _list_name: str = None
            _items: list = []

            def _getComparement(self, item: dict, condition: Condition):
                if condition.json_fields != None:
                    _field = item.get(condition.getFirst())
                    for field in condition.json_fields:
                        _field = getattr(_field, field)

                    return _field

                return item.get(condition.getFirst(), None)

            @classmethod
            def _init_operators(_cls):
                class Equals(Operator):
                    operator = '=='

                    def _implementation(self, query, condition):
                        _new = list()
                        for item in self._items:
                            if query._getComparement(item, condition) == condition.getLast():
                                _new.append(item)

                        return _new

                class In(Operator):
                    operator = 'in'

                    def _implementation(self, query, condition):
                        _new = list()
                        for item in self._items:
                            if query._getComparement(item, condition) in condition.getLast():
                                _new.append(item)

                        return _new

                _cls.operators = [Equals, In]

            def _applyCondition(self, condition):
                for val in self.operators:
                    if condition.operator == val.operator:
                        self._items = val()(self, condition)
                        return self

                return self

            # TODO
            def _applySort(self, sort: Sort):
                return self

            def _applyLimits(self):
                if self.getLimit() != None:
                    self._items = self._items[0:abs(self.getLimit())]

                return self

            def first(self):
                self._items = self._get_list()
                self._apply()

                return self._model.from_json(self._items[0])

            def count(self):
                return len(self._items)

            def _get_list(self):
                return self_adapter.data.get(self._list_name)

            def getAll(self):
                self._items = self._get_list()
                self._apply()

                for item in self._items:
                    yield self._model.from_json(item)

        self_adapter.QueryAdapter = QueryAdapter

        class _LinkAdapter(LinkAdapter):
            _adapter = self_adapter
            uuid: int = None
            owner: int = None
            target: int = None
            data: dict[str] = {}
            order: int = None

            def reorder(self, order: int = 0):
                self.order = order
                self_adapter.commit()

            def getTarget(self):
                _obj = _ObjectAdapter.getById(self.target)
                if _obj == None:
                    return self.fallback()

                return _obj

            @classmethod
            def getQuery(cls):
                _query = self_adapter.QueryAdapter()
                _query._model = cls
                _query._list_name = 'links'

                return _query

            def toDB(self, owner, link: CommonLink):
                assert link.item.hasDb(), 'link item is not flushed'
                assert self.getStorageItemName() == link.item._db.getStorageItemName(), 'cross db'

                self.owner = owner.uuid
                self.target = link.item.getDbId()
                self.uuid = next(self_adapter._id_gen)
                if link.data != None:
                    self.data = link.data

                link.setDb(self)
                # self_adapter.log(f"flushed link with target uuid {link.item.getDbId()}")
                self_adapter.data.get('links').append(self.to_json())

                if owner._orig != None:
                    owner._orig.save()

                if self_adapter.auto_commit == True:
                    self_adapter.commit()

            def _parseRoles(self) -> list:
                return self.data.get('role')

            # no pydantic today
            @staticmethod
            def from_json(data: dict):
                _obj = _LinkAdapter()
                _obj.uuid = data.get('uuid')
                _obj.owner = data.get('owner')
                _obj.target = data.get('target')
                _obj.data = LinkData(**data.get('data'))
                _obj.order = data.get('order')

                return _obj

            def to_json(self):
                return {
                    'uuid': self.uuid,
                    'owner': self.owner,
                    'target': self.target,
                    'data': self.data.to_minimal_json(),
                    'order': self.order,
                }

        class _ObjectAdapter(ObjectAdapter):
            _adapter = self_adapter
            _orig = None

            uuid: int = None
            content: dict = None

            def toDB(self, obj: Object):
                self._orig = obj
                self.flush_content(self._orig)
                self.uuid = next(self_adapter._id_gen)

                self_adapter.data.get('objects').append(self.to_json())

                if self_adapter.auto_commit == True:
                    self_adapter.commit()

            def _parseJson(self):
                return self.to_json().get('content')

            def to_json(self):
                return {
                    'uuid': self.uuid,
                    'content': self.content
                }

            @staticmethod
            def from_json(data: dict):
                _obj = _ObjectAdapter()
                _obj.uuid = data.get('uuid')
                _obj.content = data.get('content')

                return _obj

            def flush_content(self, obj: Object = None):
                if obj == None:
                    obj = self._orig

                self.content = obj.to_extended_json()

            def getLinks(self) -> Generator[CommonLink]:
                _query = self_adapter.QueryAdapter()
                _query._model = _LinkAdapter
                _query._list_name = 'links'
                _query.addCondition(Condition(
                    val1 = Value(
                        column = 'owner'
                    ),
                    operator = '==',
                    val2 = Value(
                        value = self.uuid
                    )
                ))

                for link in _query.getAll():
                    _res = link.toPython()
                    if link == None or _res == None:
                        yield CommonLink(
                            item = UnknownObject()
                        )
                        continue

                    yield _res

            @classmethod
            def getQuery(cls):
                _query = self_adapter.QueryAdapter()
                _query._model = cls
                _query._list_name = 'objects'

                return _query

            def addLink(self, link: CommonLink):
                _link = _LinkAdapter()
                _link.toDB(self, link)

                return _link

            def removeLink(self, link: CommonLink):
                link.delete()

            def deleteFromDB(self, remove_links: bool = True):
                for item in self.getLinks():
                    item.delete()

        self_adapter.ObjectAdapter = _ObjectAdapter
        self_adapter.LinkAdapter = _LinkAdapter

    def _check_file(self, path: str):
        _path = Path(path)
        if _path.exists() == False:
            _tmp = open(_path, 'w', encoding='utf-8')
            _tmp.close()

        self._stream = open(str(_path), 'r+', encoding='utf-8')

    def commit(self):

        if self._stream != None:
            self._stream.truncate(0)
            self._stream.seek(0)
            self._stream.write(json.dumps(self.data, indent = self.indent) + '\n')
            self._stream.flush()
        else:
            self.log('this objectslist is fileless')

    def _init_hook(self):
        self._set_id_gen()
        self._init_models()

        self.data = {
            'objects': [],
            'links': [],
        }

        if self.file != None:
            self._check_file(self.file)
            _read = self._stream.read()
            try:
                _json = json.loads(_read)

                self.data['objects'] = _json.get('objects')
                self.data['links'] = _json.get('links')
            except:
                pass

    def destroy(self):
        self._stream.close()
