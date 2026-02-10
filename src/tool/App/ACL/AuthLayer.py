from App.Objects.Object import Object
from App.Objects.Arguments.ListArgument import ListArgument
from App.Objects.Arguments.Argument import Argument
from pydantic import Field
from typing import Generator
from Data.Boolean import Boolean
from App.ACL.User import User
from App.ACL.Permissions.Permission import Permission
from App.DB.Query.Condition import Condition
from App import app

class AuthLayer(Object):
    def getUserByName(self, name: str) -> User:
        for item in self.getUsers():
            if item.name == name:
                return item

    def login(self, name: str, password: str, login_from: str = None):
        user = self.getUserByName(name)

        assert user != None, 'user not found'
        _usr = user.auth(password)
        assert _usr, 'invalid username or password'

        _role = ['auth_as']
        if login_from != None:
            _role.append('auth_from_' + login_from)

        self.log(f"logged as {name}", role = _role)

        return user

    def getUsers(self) -> Generator[User]:
        _storage = app.Storage.get('users')
        _query = _storage.adapter.getQuery()
        _query.addCondition(Condition(
            val1 = 'content',
            operator = '==',
            val2 = 'App.ACL.User',
            json_fields = ['obj', 'saved_via', 'object_name']
        ))

        for user in _query.getAll():
            yield user.toPython()

    def add_user(self, user: User):
        user.flush(app.Storage.get('users'))

    @classmethod
    def mount(cls):
        _layer = cls()

        # App.Objects.Index.PostRun will check root user
        app.mount('AuthLayer', _layer)

    @classmethod
    def _settings(cls):
        return [
            Argument(
                name = 'app.auth.every_call_permission_check',
                default = False,
                orig = Boolean
            )
        ]
