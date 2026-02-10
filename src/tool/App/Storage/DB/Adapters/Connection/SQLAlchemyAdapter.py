from App.Storage.DB.Adapters.ConnectionAdapter import ConnectionAdapter
from App.Storage.DB.Adapters.ObjectAdapter import ObjectAdapter
from App.Storage.DB.Adapters.ObjectLinkAdapter import ObjectLinkAdapter
from App.Objects.Object import Object
from App.Objects.Link import Link as CommonLink
from snowflake import SnowflakeGenerator
from typing import Any, Generator
import json

class SQLAlchemyAdapter(ConnectionAdapter):
    _engine: Any = None
    _session: Any = None
    ObjectUnit: Any = None
    ObjectUnitLink: Any = None

    @classmethod
    def getRequiredModules(self):
        return ['sqlalchemy==2.0.44', 'snowflake-id']

    def _init_models(self):
        from sqlalchemy.ext.declarative import declarative_base
        from sqlalchemy import Column, Integer, event, String

        Base = declarative_base()
        session = self._session

        _id_gen = SnowflakeGenerator(32)

        class ObjectUnit(ObjectAdapter, Base):
            __tablename__ = 'objects'
            uuid = Column(Integer(), primary_key=True)
            content = Column(String(), nullable=False)

            class Link(ObjectLinkAdapter, Base):
                __tablename__ = 'links'
                uuid = Column(Integer(), primary_key=True)
                owner = Column(Integer())
                target = Column(Integer())
                role = Column(String(), nullable = True)

                def getTarget(self):
                    return ObjectUnit.getById(self.target)

                @classmethod
                def getById(cls, id: int):
                    return session.query(cls).filter(cls.uuid == id).first()

            @classmethod
            def getById(cls, id: int):
                return session.query(cls).filter(cls.uuid == id).first()

            @classmethod
            def getQuery(cls):
                return session.query(cls)

            def getLinks(self) -> Generator[CommonLink]:
                links = session.query(self.Link).filter(self.Link.owner == self.uuid)
                for link in links:
                    yield link.getLink()

            def addLink(self, link):#, session):
                _link = self.Link()
                link.setDb(_link)

                _link.owner = self.uuid
                _link.target = link.item.getDbId()
                if len(link.role) > 0:
                    _link.role = str(link.role)

                session.add(_link)
                session.commit()

            def removeLink(self, link):
                pass

            def flush_content(self, obj: Object):
                _data = obj.to_json(
                    exclude_internal = True,
                    exclude = ['links'],
                    convert_links = False,
                    exclude_none = True
                )
                self.content = json.dumps(_data)

            def flush(self, 
                      obj: Object, 
                      current_level: int = 0, 
                      max_depth: int = 10):

                self.flush_content(obj)

                session.add(self)
                session.commit()

                if current_level < max_depth:
                    for link in obj.getLinkedItems():
                        _obj = self.__class__()
                        _obj.flush(
                            obj = link.item,
                            current_level = current_level + 1,
                            max_depth = max_depth
                        )

                        self.addLink(link = link)

                obj.setDb(self)
                self.flush_content(obj)
                session.commit()

        @event.listens_for(ObjectUnit, 'before_insert', propagate=True)
        @event.listens_for(ObjectUnit.Link, 'before_insert', propagate=True)
        def receive_before_insert(mapper, connection, target):
            if target.uuid is None:
                target.uuid = next(_id_gen)

        self.ObjectUnit = ObjectUnit

        Base.metadata.create_all(self._engine)

    def flush(self, obj: Object):
        unit = self.ObjectUnit()
        unit.flush(obj)

        return unit

    def search(self):
        pass

    def _get_engine(self, connection_str: str):
        pass
