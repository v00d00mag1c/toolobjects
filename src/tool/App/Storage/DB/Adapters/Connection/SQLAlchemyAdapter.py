from App.Storage.DB.Adapters.ConnectionAdapter import ConnectionAdapter
from App.Storage.DB.Adapters.ObjectAdapter import ObjectAdapter
from App.Storage.DB.Adapters.ObjectLinkAdapter import ObjectLinkAdapter
from App.Objects.Object import Object
from App.Objects.Link import Link as CommonLink
from typing import Any, Generator
import json

class SQLAlchemyAdapter(ConnectionAdapter):
    _engine: Any = None
    _session: Any = None

    @classmethod
    def getRequiredModules(cls):
        return ['sqlalchemy==2.0.44', 'snowflake-id']

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

    def _init_models(self_adapter):
        from sqlalchemy.ext.declarative import declarative_base
        from sqlalchemy import Column, Integer, event, String

        Base = declarative_base()
        session = self_adapter._session
        _id_gen = self_adapter._id_gen

        # a lot of confusing links
        class _ObjectAdapter(ObjectAdapter, Base):
            __tablename__ = 'objects'
            _adapter = self_adapter

            uuid = Column(Integer(), primary_key=True)
            content = Column(String(), nullable=False)

            class Link(ObjectLinkAdapter, Base):
                __tablename__ = 'links'
                _adapter = self_adapter

                uuid = Column(Integer(), primary_key=True)
                owner = Column(Integer())
                target = Column(Integer())
                role = Column(String(), nullable = True)

                def getTarget(self):
                    return _ObjectAdapter.getById(self.target)

                @classmethod
                def getById(cls, id: int):
                    return session.query(cls).filter(cls.uuid == id).first()

                def flush(self, owner, link: CommonLink):
                    assert link.item.hasDb(), 'link item is not flushed.'

                    self.owner = owner.uuid
                    self.target = link.item.getDbId()
                    if len(link.role) > 0:
                        self.role = str(link.role)

                    session.add(self)

            @classmethod
            def getById(cls, id: int):
                return cls.getQuery().filter(cls.uuid == id).first()

            @classmethod
            def getQuery(cls):
                return session.query(cls)

            # Flush functions
            def flush(self, 
                      obj: Object):

                session.add(self)
                self.flush_content(obj)

            def flush_content(self, obj: Object):
                _data = obj.to_json(
                    exclude_internal = False,
                    exclude = ['links', 'db_info', 'class_name'],
                    convert_links = False,
                    exclude_none = True
                )
                self.content = json.dumps(_data)
                session.commit()

            # Link functions
            def getLinks(self) -> Generator[CommonLink]:
                links = session.query(self.Link).filter(self.Link.owner == self.uuid)
                for link in links:
                    yield link.getLink()

            def addLink(self, link: CommonLink):#, session):
                '''
                Creates link from current object adapter to another object (that already flushed)
                '''

                _link = self.Link()
                _link.flush(self, link)
                session.commit()

                return _link

            def removeLink(self, link):
                pass

        @event.listens_for(_ObjectAdapter, 'before_insert', propagate=True)
        @event.listens_for(_ObjectAdapter.Link, 'before_insert', propagate=True)
        def receive_before_insert(mapper, connection, target):
            if target.uuid is None:
                target.uuid = next(_id_gen)

        self_adapter.ObjectAdapter = _ObjectAdapter
        self_adapter.ObjectLinkAdapter = _ObjectAdapter.Link

        Base.metadata.create_all(self_adapter._engine)
