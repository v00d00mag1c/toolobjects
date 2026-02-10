from App.Objects.Mixins.BaseModel import BaseModel
from pydantic import Field
from typing import Literal
from App import app
from App.DB.Query.Condition import Condition

class Permission(BaseModel):
    object_name: str = Field()
    user: str = Field()
    uuid: int = Field(default = None)
    action: Literal['view', 'delete', 'edit', 'link', 'call'] = Field(default = 'call')
    allow: bool = Field(default = True)

    # TODO: rewrite
    @classmethod
    def getPermissions(cls, likeness: BaseModel = None):
        _storage = app.Storage.get('users')
        _query = _storage.adapter.getQuery()
        _query.addCondition(Condition(
            val1 = 'content',
            operator = '==',
            val2 = 'App.ACL.Permissions.Permission',
            json_fields = ['obj', 'saved_via', 'object_name']
        ))

        if likeness != None:
            for key in ['object_name', 'user', 'action', 'allow', 'uuid']:
                if getattr(likeness, key, None) != None:
                    _query.addCondition(Condition(
                        val1 = 'content',
                        operator = '==',
                        val2 = getattr(likeness, key, None),
                        json_fields = [key]
                    ))

        return _query.getAll()

    @classmethod
    def check(cls, likeness: BaseModel = None):
        return len(list(cls.getPermissions(likeness))) > 0
