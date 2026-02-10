from App.Objects.Object import BaseModel
from App.DB.DBInsertable import DBInsertable
from pydantic import Field
from typing import Literal, Optional
from App import app
from App.DB.Query.Condition import Condition

class Permission(BaseModel, DBInsertable):
    object_name: str = Field()
    user: Optional[str] = Field(default = None)
    uuid: int = Field(default = None)
    action: Literal['view', 'delete', 'edit', 'link', 'call'] = Field(default = 'call')
    allow: bool = Field(default = True)

    # TODO: rewrite
    @classmethod
    def getPermissions(cls, likeness: BaseModel = None):
        _storage = app.Storage.get('users')
        _query = _storage.adapter.getQuery()
        _query.where_object(cls)

        if likeness != None:
            for key in ['object_name', 'user', 'action', 'allow', 'uuid']:
                if getattr(likeness, key, None) != None:
                    _query.addCondition(Condition(
                        val1 = 'content',
                        operator = '==',
                        val2 = getattr(likeness, key),
                        json_fields = [key]
                    ))

        return _query

    @classmethod
    def check(cls, likeness: BaseModel = None):
        return cls.getPermissions(likeness).count() > 0
