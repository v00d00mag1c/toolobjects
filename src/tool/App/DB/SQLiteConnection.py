from App.Objects.Object import Object
from pydantic import Field
from typing import Any
import json

class SQLiteConnection(Object):
    content: str = Field(default = None)
    engine: Any = None
    _content_unit: Any = None

    def constructor(self):
        from sqlalchemy import create_engine
        from sqlalchemy import MetaData, Table, Column, Integer, String

        _connection_str = "sqlite:///"
        if self.content != None:
            _connection_str += self.content

        self.engine = create_engine(_connection_str)
        metadata_obj = MetaData()

        self._content_unit = Table(
            "items",
            metadata_obj,
            Column("uuid", Integer, primary_key=True),
            Column("content", String(), nullable=False)
        )

        metadata_obj.create_all(self.engine)

    def passObject(self, obj):
        from sqlalchemy import insert

        with self.engine.connect() as conn:
            conn.execute(insert(self._content_unit).values(uuid=0, content = json.dumps(obj.to_json())))
            conn.commit()
