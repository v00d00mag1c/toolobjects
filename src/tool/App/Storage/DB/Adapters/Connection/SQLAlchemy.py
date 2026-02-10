from App.Storage.DB.Adapters.ConnectionAdapter import ConnectionAdapter
from App.Storage.DB.Adapters.Representation.ObjectAdapter import ObjectAdapter
from App.Storage.DB.Adapters.Representation.LinkAdapter import LinkAdapter
from App.Storage.DB.Adapters.Search.Query import Query
from App.Storage.DB.Adapters.Search.Condition import Condition
from App.Storage.DB.Adapters.Search.Sort import Sort
from App.Objects.Object import Object
from App.Objects.Relations.Link import Link as CommonLink
from App.Objects.Requirements.Requirement import Requirement
from typing import Any, Generator
import json

class SQLAlchemy(ConnectionAdapter):
    class QueryAdapter(Query):
        def _getComparement(self, condition: Condition):
            return getattr(self._model, condition.getFirst())

        # naaah
        def _op_equals(self, condition):
            return self._query.filter(self._getComparement(condition) == condition.getLast())

        def _op_in(self, condition):
            return self._query.filter(self._getComparement(condition).in_(condition.getLast()))

        def _op_not_in(self, condition):
            return self._query.filter(self._getComparement(condition).not_in_(condition.getLast()))

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

        def addSorting(self, sort: Sort):
            from sqlalchemy import desc

            if sort.descend == True:
                self._query = self._query.order_by(self._getComparement(sort.condition))
            else:
                self._query = self._query.order_by(desc(self._getComparement(sort.condition)))

            return self

        def first(self):
            return self._query.first()

        def getAll(self):
            for item in self._query:
                yield item

        def limit(self, limit: int):
            self._query = self._query.limit(limit)
            return self

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
                return _ObjectAdapter.getById(self.target)

            @classmethod
            def getQuery(cls):
                _query = self_adapter.QueryAdapter()
                _query._model = cls
                _query._query = _session.query(cls)

                return _query

            def toDB(self, owner, link: CommonLink):
                assert link.item.hasDb(), 'link item is not flushed.'

                self.owner = owner.uuid
                self.target = link.item.getDbId()
                if len(link.role) > 0:
                    self.role = str(link.role)

                _session.add(self)

        # a lot of confusing links
        class _ObjectAdapter(ObjectAdapter, Base):
            __tablename__ = 'objects'
            _adapter = self_adapter

            uuid = Column(Integer(), primary_key=True)
            content = Column(String(), nullable=False)

            def toDB(self, obj: Object):
                _session.add(self)
                self.flush_content(obj)

            def flush_content(self, obj: Object):
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
                links = _session.query(_LinkAdapter).filter(self.Link.owner == self.uuid)
                for link in links:
                    yield link.getLink()

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
    def getRequiredModules(cls):
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
