from App.DB.ConnectionAdapter import ConnectionAdapter
from App.DB.Representation.ObjectAdapter import ObjectAdapter
from App.DB.Representation.LinkAdapter import LinkAdapter
from App.DB.Query.Query import Query
from App.DB.Query.Condition import Condition
from App.DB.Query.Sort import Sort
from App.DB.Query.Values.Value import Value
from App.Objects.Object import Object
from App.Objects.Relations.Link import Link as CommonLink
from App.Objects.Requirements.Requirement import Requirement
from App.Objects.Misc.UnknownObject import UnknownObject
from App.Objects.Misc.Increment import Increment
from App.DB.Query.Operator import Operator
from App.DB.Query.Function import Function
from typing import Any, Generator, ClassVar
from pydantic import Field
import json

class SQLAlchemy(ConnectionAdapter):
    _engine: Any = None
    _session: Any = None
    delimiter: ClassVar[str] = '://'

    # OK, its very bad code, but however
    def _get_content_column(self):
        from sqlalchemy import Column, Text

        return Column(Text(), nullable=False)

    # we have to put this into function to have links to the connection class and session)
    def _init_models(self_adapter):
        from sqlalchemy.ext.declarative import declarative_base
        from sqlalchemy import Column, BigInteger, Integer, event, String

        Base = declarative_base()

        class _LinkAdapter(LinkAdapter, Base):
            __tablename__ = self_adapter.links_table_name
            _adapter = self_adapter

            uuid = Column(BigInteger(), primary_key=True, index=True)
            owner = Column(BigInteger(), nullable = True, index=True) # if null its links to db
            target = Column(BigInteger())
            data = Column(String(1000), nullable = True)
            order = Column(BigInteger())

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
                _query._query = self_adapter.getSession().query(cls)

                return _query

            def toDB(self, owner, link: CommonLink, order: Increment):
                assert link.item.hasDb(), 'link item is not flushed'
                #assert self.getStorageItemName() == link.item._db.getStorageItemName(), 'cross db'

                self.owner = owner.uuid
                self.target = link.item.getDbId()
                self.order = order.getIndex()
                if len(link.data.role) > 0:
                    self.data = json.dumps(link.data.to_minimal_json())

                link.setDb(self)
                # self_adapter.log(f"flushed link with target uuid {link.item.getDbId()}")

                if owner._orig != None:
                    owner._orig.save()

                if self.uuid is None:
                    self.uuid = next(self_adapter._id_gen)

                self_adapter.getSession().add(self)

            def fallback(self):
                return None

            def deleteFromDB(self, remove_links: bool = True):
                from sqlalchemy import delete

                self_adapter.getSession().delete(self)
                if self_adapter.auto_commit == True:
                    self_adapter.commit()

        # a lot of confusing links
        class _ObjectAdapter(ObjectAdapter, Base):
            __tablename__ = self_adapter.objects_table_name
            _adapter = self_adapter
            _orig = None
            order_index = None

            uuid = Column(BigInteger(), primary_key=True, index=True)
            content = self_adapter._get_content_column()

            def get_order_index(self):
                if self.order_index == None:
                    self.order_index = Increment(value = 0)

                    if self.uuid != None:
                        self.order_index.move(self_adapter.getSession().query(_LinkAdapter).filter(_LinkAdapter.owner == self.uuid).count())

                return self.order_index

            def toDB(self, obj: Object, ignore_content: bool = True):
                if self.uuid is None:
                    self.uuid = next(self_adapter._id_gen)

                self_adapter.getSession().add(self)
                self.get_permission_to_flush(obj)
                self._orig = obj

                self.content = json.dumps({'flush': 'notflushed'})

            def flush_content(self, obj: Object = None):
                if obj == None:
                    obj = self._orig

                self.content = json.dumps(obj.to_db_json())
                if self_adapter.auto_commit == True:
                    self_adapter.commit()

            # Link functions
            def getLinks(self, with_role: str = None) -> Generator[CommonLink]:
                from sqlalchemy import func

                _query = self_adapter.QueryAdapter()
                _query._query = self_adapter.getSession().query(_LinkAdapter)
                _query._model = _LinkAdapter
                _query.addCondition(Condition(
                    val1 = Value(
                        column = 'owner'
                    ),
                    operator = '==',
                    val2 = Value(
                        value = self.uuid
                    )
                ))
                #if with_role:
                #    _query._query = _query._query.select_from(func.json_each(func.json_extract(_LinkAdapter.data, '$.role'))).where(func.json_each.c.value == with_role)

                _query.addSort(Sort(
                    condition = Condition(
                        val1 = Value(
                            column = 'order'
                        )
                    )
                ))
                for link in _query.getAll():
                    yield link

            @classmethod
            def getQuery(cls):
                _query = self_adapter.QueryAdapter()
                _query._model = cls
                _query._query = self_adapter.getSession().query(cls)

                return _query

            def addLink(self, link: CommonLink, no_commit: bool = False):
                _link = _LinkAdapter()
                _link.toDB(self, link, self.get_order_index())

                if self_adapter.auto_commit == True and no_commit == False:
                    self_adapter.commit()

                return _link

            def removeLink(self, link: CommonLink):
                _query = self_adapter.QueryAdapter()
                _query._query = self_adapter.getSession().query(_LinkAdapter)
                _query._model = _LinkAdapter
                _query.addCondition(Condition(
                    val1 = Value(
                        column = 'owner'
                    ),
                    operator = '==',
                    val2 = Value(
                        value = self.uuid
                    )
                ))
                _query.addCondition(Condition(
                    val1 = Value(
                        column = 'target'
                    ),
                    operator = '==',
                    val2 = Value(
                        value = link.item.getDbId()
                    )
                ))
                if len(link.data.role) > 0:
                    _query.addCondition(Condition(
                        val1 = Value(
                            column = 'data',
                            json_fields = ['role']
                        ),
                        operator = '==',
                        val2 = Value(
                            value = json.dumps(link.data.role)
                        )
                    ))

                _items = list(_query.getAll())
                self_adapter.log('links remover: found {0} items'.format(len(_items)))

                for item in _items:
                    item.toPython().delete()

            def deleteFromDB(self, remove_links: bool = True):
                from sqlalchemy import delete

                if remove_links == True:
                    for item in self.getLinks():
                        item.delete()

                self_adapter.getSession().delete(self)
                if self_adapter.auto_commit == True:
                    self_adapter.commit()

        self_adapter.ObjectAdapter = _ObjectAdapter
        self_adapter.LinkAdapter = _LinkAdapter

        Base.metadata.create_all(self_adapter._engine)

    class QueryAdapter(Query):
        _model: Any = None
        _query: Any = None

        @classmethod
        def _init_operators(_cls):
            # idk how to shrink this
            class OperatorOverride(Operator):
                def _condition_get(self, query, db_query, condition):
                    pass
                    #return self._condition_get(query, db_query, condition) == query._get_part(condition, 1)

                def _implementation(self, query, db_query, condition):
                    return db_query.filter(self._condition_get(query, db_query, condition))

            class Equals(OperatorOverride):
                operator = '=='

                def _condition_get(self, query, db_query, condition):
                    return query._get_part(condition) == query._get_part(condition, 1)

            class NotEquals(OperatorOverride):
                operator = '!='

                def _condition_get(self, query, db_query, condition):
                    return query._get_part(condition) != query._get_part(condition, 1)

            class In(OperatorOverride):
                operator = 'in'

                def _condition_get(self, query, db_query, condition):
                    return query._get_part(condition).in_(query._get_part(condition, 1))

            class NotIn(OperatorOverride):
                operator = 'not_in'

                def _condition_get(self, query, db_query, condition):
                    return query._get_part(condition).not_in(query._get_part(condition, 1))

            class Lesser(OperatorOverride):
                operator = '<'

                def _condition_get(self, query, db_query, condition):
                    return query._get_part(condition) < query._get_part(condition, 1)

            class Greater(OperatorOverride):
                operator = '>'

                def _condition_get(self, query, db_query, condition):
                    return query._get_part(condition) > query._get_part(condition, 1)

            class LesserOrEqual(OperatorOverride):
                operator = '<='

                def _condition_get(self, query, db_query, condition):
                    return query._get_part(condition) <= query._get_part(condition, 1)

            class GreaterOrEqual(OperatorOverride):
                operator = '>='

                def _condition_get(self, query, db_query, condition):
                    return query._get_part(condition) >= query._get_part(condition, 1)

            class Contains(OperatorOverride):
                operator = 'contains'

                def _condition_get(self, query, db_query, condition):
                    return query._get_part(condition).contains(query._get_part(condition, 1))

            class Mod(Function):
                operator = '%'

                def _implementation(self, value_item, column, value):
                    return column % value_item.args[0]

            class JSONContains(Function):
                operator = 'json_contains'

                def _implementation(self, value_item, column, value):
                    from sqlalchemy import func

                    return getattr(func, self.operator)(column, value)

            class JSONEach(JSONContains):
                operator = 'json_each'

            class Random(Function):
                operator = 'random'

                def _implementation(self, value_item, column, value):
                    from sqlalchemy import func

                    return func.random()

            _cls.operators = [Equals, NotEquals, In, NotIn, Lesser, Greater, LesserOrEqual, GreaterOrEqual, Contains]
            _cls.functions = [Mod, Random, JSONContains, JSONEach]

        # Method that receives part from condition
        def _get_part(self, condition: Condition, val_num: int = 0):
            _item = None
            if val_num == 0:
                _item = condition.getFirst()
            elif val_num == 1:
                _item = condition.getLast()

            if _item == None:
                return None

            if _item.column != None:
                _val = None
                # wont move to function
                if _item.json_fields != None:
                    _val = self._json_value(_item)
                else:
                    _val = getattr(self._model, _item.column)

                if _item.func:
                    for _func in self.functions:
                        if _func.operator == _item.func:
                            return _func()._implementation(_item, _val, self._get_part(condition, 1))

                return _val

            if _item.value != None:
                return _item.value

        def _json_value(self, item):
            from sqlalchemy import func

            _fields = '.'.join(item.json_fields)
            return func.json_extract(getattr(self._model, item.column), '$.' + _fields)

        def _applyCondition(self, condition):
            for val in self.operators:
                if condition.operator == val.operator:
                    self._query = val()._implementation(self, self._query, condition)

                    return self

            self.log('error: can\'t find operator function')

            # This won't work, but we can't get further
            self._query = getattr(self, condition.operator)(condition)
            return self

        def _applyOrCondition(self, conditions):
            from sqlalchemy import or_

            conds = list()
            for condition in conditions:
                for val in self.operators:
                    if condition.operator == val.operator:
                        conds.append(val()._condition_get(self, self._query, condition))

            self._query = self._query.filter(or_(*conds))

        def _applySort(self, sort: Sort):
            from sqlalchemy import desc

            if sort.descend == False:
                self._query = self._query.order_by(self._get_part(sort.condition))
            else:
                self._query = self._query.order_by(desc(self._get_part(sort.condition)))

            return self

        def _applyLimits(self):
            self._query = self._query.limit(self.getLimit())

            return self._query

        def first(self):
            self._apply()

            return self._query.first()

        def count(self):
            self._apply()

            return self._query.count()

        def getAll(self):
            self._apply()

            for item in self._query:
                yield item

    @classmethod
    def _requirements(cls):
        return [
            Requirement(
                name = 'sqlalchemy',
                version = '2.0.44'
            ),
            Requirement(
                name = 'SQLAlchemy-Utils'
            ),
            Requirement(
                name = 'snowflake-id'
            )
        ]

    def _before_init_models(self):
        pass

    def _init_hook(self):
        self._set_id_gen()
        self._get_engine(self._get_sqlalchemy_connection_string_with_protocol())
        self._create_session()
        self._before_init_models()
        self._init_models()
        # self._links_count = Increment(value = self._session.query(self.LinkAdapter).count())

    def _get_sqlalchemy_connection_string(self):
        return ""

    def _get_sqlalchemy_connection_string_with_protocol(self) -> str:
        return self.protocol_name + self.delimiter + self._get_sqlalchemy_connection_string()

    def _get_engine(self, connection_str: str):
        from sqlalchemy import create_engine

        self._engine = create_engine(connection_str)

    def _create_session(self):
        from sqlalchemy.orm import Session

        self._session = Session(self._engine, expire_on_commit=False)

    def getSession(self):
        return self._session

    def commit(self):
        _role = ['db.commit']
        if self._storage_item.name == 'tmp':
            _role.append('db.commit.to_tmp')

        self.log('commit...', role = _role)

        self.getSession().commit()

    def destroy(self):
        self.getSession().close()
        self._engine.dispose()
