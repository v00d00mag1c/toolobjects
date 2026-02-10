from App.DB.ConnectionAdapters.ConnectionAdapter import ConnectionAdapter
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, event, String
from snowflake import SnowflakeGenerator
from typing import Any
import json

class SQLAlchemyAdapter(ConnectionAdapter):
    _engine: Any = None

    def _init_models(self):
        Base = declarative_base()
        class ObjectUnit(Base):
            __tablename__ = 'objects'
            uuid = Column(Integer(), primary_key=True)
            content = Column(String(), nullable=False)

        self.ObjectAdapter = ObjectUnit

        @event.listens_for(ObjectUnit, 'before_insert', propagate=True)
        def receive_before_insert(mapper, connection, target):
            if target.uuid is None:
                target.uuid = next(SnowflakeGenerator(32))

        Base.metadata.create_all(self._engine)

    def insertObject(self, obj: Any):
        from sqlalchemy.orm import Session

        unit = None

        with Session(self._engine) as session:
            unit = self.ObjectUnit(
                content=json.dumps(
                    obj.to_json()
                )
            )
            session.add(unit)
            session.commit()

        return unit

    def recieveObject(self, obj):
        _content = obj.content
        _class = app.app.list.findByName(obj.content.saved_via.object_name)

        return _class(**_content)

    def search(self):
        pass
