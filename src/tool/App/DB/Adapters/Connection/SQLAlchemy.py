from App.DB.Adapters.ConnectionAdapter import ConnectionAdapter
from App.DB.Adapters.Representation.ObjectAdapter import ObjectAdapter
from App.DB.Adapters.Representation.LinkAdapter import LinkAdapter
from App.DB.Adapters.Search.Query import Query
from App.DB.Adapters.Search.Condition import Condition
from App.DB.Adapters.Search.Sort import Sort
from App.Objects.Object import Object
from App.Objects.Relations.Link import Link as CommonLink
from App.Objects.Requirements.Requirement import Requirement
from App.Objects.Misc.UnknownObject import UnknownObject
from typing import Any, Generator
import json

class SQLAlchemy(ConnectionAdapter):
    class QueryAdapter(Query):
        _model: Any = None
        _query: Any = None

        def _getComparement(self, condition: Condition):
            return getattr(self._model, condition.getFirst())

        # naaah
        def _op_equals(self, condition):
            return self._query.filter(self._getComparement(condition) == condition.getLast())

        def _op_in(self, condition):
            return self._query.filter(self._getComparement(condition).in_(condition.getLast()))

        def _op_not_in(self, condition):
            return self._query.filter(self._getComparement(condition).not_in(condition.getLast()))

        def _op_lesser(self, condition):
            return self._query.filter(self._getComparement(condition) < condition.getLast())

        def _op_greater(self, condition):
            return self._query.filter(self._getComparement(condition) > condition.getLast())

        def _op_lesser_or_equal(self, condition):
            return self._query.filter(self._getComparement(condition) <= condition.getLast())

        def _op_greater_or_equal(self, condition):
            return self._query.filter(self._getComparement(condition) >= condition.getLast())

        def _op_contains(self, condition):
            return self._query.filter(self._getComparement(condition).contains(condition.getLast()))

        def _applyCondition(self, condition):
            for key, val in self.operators.items():
                if condition.operator == key:
                    self._query = getattr(self, val)(condition)

                    return self

            self._query = getattr(self, condition.operator)(condition)
            return self

        def _applySort(self, sort: Sort):
            from sqlalchemy import desc

            if sort.descend == True:
                self._query = self._query.order_by(self._getComparement(sort.condition))
            else:
                self._query = self._query.order_by(desc(self._getComparement(sort.condition)))

            return self

        def _applyLimits(self):
            self._query = self._query.limit(self.limits)

            return self._query

        def first(self):
            self._apply()

            return self._query.first()

        def count(self):
            return self._query.count()

        def getAll(self):
            self._apply()

            for item in self._query:
                yield item

    # we have to put this into function(
    def _init_models(self_adapter):
        from sqlalchemy.ext.declarative import declarative_base
        from sqlalchemy import Column, Integer, event, String

        Base = declarative_base()
        _session = self_adapter._session

        class _LinkAdapter(LinkAdapter, Base):
            __tablename__ = 'links'
            _adapter = self_adapter

            uuid = Column(Integer(), primary_key=True)
            owner = Column(Integer(), nullable = True) # if null its links to db
            target = Column(Integer())
            role = Column(String(), nullable = True)
            order = Column(Integer())

            def getTarget(self):
                _obj = _ObjectAdapter.getById(self.target)
                if _obj == None:
                    return self.fallback()

                return _obj

            @classmethod
            def getQuery(cls):
                _query = self_adapter.QueryAdapter()
                _query._model = cls
                _query._query = _session.query(cls)

                return _query

            def toDB(self, owner, link: CommonLink):
                assert link.item.hasDb(), 'link item is not flushed'
                assert self._adapter._storage_item.name == link.item._db._adapter._storage_item.name, 'cross db'

                self.owner = owner.uuid
                self.target = link.item.getDbId()
                if len(link.role) > 0:
                    self.role = json.dumps(link.role)

                link.setDb(self)
                self_adapter.log(f"flushed link with target uuid {link.item.getDbId()}")

                if owner._orig != None:
                    owner._orig.save()

                _session.add(self)

            def fallback(self):
                return None

        # a lot of confusing links
        class _ObjectAdapter(ObjectAdapter, Base):
            __tablename__ = 'objects'
            _adapter = self_adapter
            _orig = None

            uuid = Column(Integer(), primary_key=True)
            content = Column(String(), nullable=False)

            def toDB(self, obj: Object):
                _session.add(self)
                self._orig = obj
                self.flush_content(self._orig)

            def flush_content(self, obj: Object = None):
                if obj == None:
                    obj = self._orig

                _data = obj.to_json(
                    exclude_internal = False,
                    exclude = ['links', 'db_info', 'class_name'],
                    convert_links = False,
                    exclude_none = True,
                    exclude_defaults = True,
                    only_class_fields = False
                )
                self.content = json.dumps(_data)
                _session.commit()

            # Link functions
            def getLinks(self) -> Generator[CommonLink]:
                links = _session.query(_LinkAdapter).filter(_LinkAdapter.owner == self.uuid)
                for link in links:
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
                _query._query = _session.query(cls)

                return _query

            def addLink(self, link: CommonLink):
                _link = _LinkAdapter()
                _link.toDB(self, link)
                _session.commit()

                return _link

            def removeLink(self, link: CommonLink):
                pass

            def deleteFromDB(self, remove_links: bool = True):
                from sqlalchemy import delete
                for item in self.getLinks():
                    item.delete()
                _session.delete(self)

        # Automatically sets snowflake id
        @event.listens_for(_ObjectAdapter, 'before_insert', propagate=True)
        @event.listens_for(_LinkAdapter, 'before_insert', propagate=True)
        def receive_before_insert(mapper, connection, target):
            if target.uuid is None:
                target.uuid = next(self_adapter._id_gen)

        self_adapter.ObjectAdapter = _ObjectAdapter
        self_adapter.LinkAdapter = _LinkAdapter

        Base.metadata.create_all(self_adapter._engine)

    @classmethod
    def _required_modules(cls):
        return [
            Requirement(
                name = 'sqlalchemy',
                version = '2.0.44'
            ),
            Requirement(
                name = 'snowflake-id'
            )
        ]

    def _constructor(self):
        connection_string = self.protocol_name + self.delimiter + self.getConnectionStringContent()

        self._set_id_get()
        self._get_engine(connection_string)
        self._init_models()

    def _get_engine(self, connection_str: str):
        from sqlalchemy import create_engine
        from sqlalchemy.orm import Session

        self._engine = create_engine(connection_str)
        self._session = Session(self._engine, expire_on_commit=False)

    _engine: Any = None
    _session: Any = None
