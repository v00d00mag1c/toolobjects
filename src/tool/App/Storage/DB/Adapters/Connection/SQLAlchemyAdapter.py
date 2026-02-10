from App.Storage.DB.Adapters.ConnectionAdapter import ConnectionAdapter
from App.Storage.DB.Adapters.ObjectAdapter import ObjectAdapter
from App.Objects.Object import Object
from App.Objects.Link import Link
from snowflake import SnowflakeGenerator
from typing import Any
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
        _id_gen = SnowflakeGenerator(32)

        class ObjectUnit(ObjectAdapter, Base):
            __tablename__ = 'objects'
            uuid = Column(Integer(), primary_key=True)
            content = Column(String(), nullable=False)

        class ObjectUnitLink(ObjectAdapter, Base):
            __tablename__ = 'links'
            uuid = Column(Integer(), primary_key=True)
            owner = Column(Integer())
            target = Column(Integer())
            role = Column(String())

        @event.listens_for(ObjectUnit, 'before_insert', propagate=True)
        @event.listens_for(ObjectUnitLink, 'before_insert', propagate=True)
        def receive_before_insert(mapper, connection, target):
            if target.uuid is None:
                target.uuid = next(_id_gen)

        self.ObjectUnit = ObjectUnit
        self.ObjectUnitLink = ObjectUnitLink

        Base.metadata.create_all(self._engine)

    def _get_engine(self, connection_str: str):
        pass

    def _flush_single(self, obj: Object):
        _item = self.ObjectUnit(
            content=json.dumps(
                obj.to_json(exclude_internal = False)
            )
        )
        obj.setDb(_item)

        return _item

    def _flush_link(self, owner, link: Link):
        print(owner, owner._db, owner._db.uuid)
        _item = self.ObjectUnitLink(
            owner = owner.getDbId(),
            target = link.item.getDbId(),
            role = str(link.role)
        )
        link.setDb(_item)

        return _item

    def flush(self, obj: Object, current_level: int = 0, max_depth: int = 10):
        unit = None
        with self._session as session:
            unit = self._flush_single(obj)
            session.add(unit)

            if current_level < max_depth:
                _links = obj.getLinkedItems()
                self.log(f'found links: {len(_links)}, current_level = {current_level} to {max_depth}')

                for link in _links:
                    self.flush(
                        obj = link.item,
                        current_level = current_level + 1,
                        max_depth = max_depth
                    )

            # idk
            if current_level == 0:
                self.log('commiting changes')

                session.commit()

            # iterating da links again to put them with ids

            if current_level == 0:
                _links = obj.getLinkedItems()
                for link in _links:
                    session.add(self._flush_link(obj, link))

                session.commit()

            return unit

    def search(self):
        pass
