from App.Objects.Object import Object
from App.Objects.Arguments.ListArgument import ListArgument
from App.Objects.Arguments.Argument import Argument
from pydantic import Field
from typing import Generator
from App.ACL.User import User
from App.ACL.Permissions.Permission import Permission
from App.ACL.Tokens.Token import Token
from App.DB.Query.Condition import Condition
from App.DB.Query.Values.Value import Value
from App import app
from Data.Types.Boolean import Boolean
from Data.Types.Float import Float

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

        _role = ['auth']
        if login_from != None:
            _role.append('auth.from_' + login_from)

        self.log(f"logged as {name}", role = _role)

        return user

    def byToken(self, token: str):
        _storage = app.Storage.get('users')
        _query = _storage.adapter.getQuery()
        _query.where_object(Token)
        _query.addCondition(Condition(
            val1 = Value(
                column = 'content',
                json_fields = ['value']
            ),
            operator = '==',
            val2 = Value(
                value = token
            ),
        ))

        _item = _query.first()
        if _item != None:
            _token = _item.toPython()
            _user = _token.to_user()
            self.log(f"logged as {_user.name}", role = ['auth', 'auth.by_token'])

            return _user

    def getUsers(self) -> Generator[User]:
        _storage = app.Storage.get('users')
        _query = _storage.adapter.getQuery()
        _query.where_object(User)

        for user in _query.getAll():
            yield user.toPython()

    def add_user(self, user: User):
        user.flush(app.Storage.get('users'))
        user.save()

    def add_permission(self, permission: Permission):
        permission.flush(app.Storage.get('users'))
        permission.save()

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
            ),
            Argument(
                name = 'app.auth.token.life',
                default = 7199,
                orig = Float
            ),
            Argument(
                name = 'app.auth.token.refresh_limit',
                default = 86400,
                orig = Float
            )
        ]
