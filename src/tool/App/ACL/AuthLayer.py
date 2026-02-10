from App.Objects.Object import Object
from App.Objects.Arguments.ListArgument import ListArgument
from App.Objects.Arguments.Argument import Argument
from pydantic import Field
from typing import Generator
from Data.Boolean import Boolean
from App.ACL.User import User
from App.ACL.Permissions.ObjectPermission import ObjectPermission
from App.ACL.GetHash import GetHash
from App import app

class AuthLayer(Object):
    users: list[User] = Field(default = [])

    def addUser(self, user: User):
        self.users.append(user)

    def getUserByName(self, name: str) -> User:
        for item in self.users:
            if item.name == name:
                return item

    def login(self, name: str, password: str):
        user = self.getUserByName(name)

        assert user != None, 'user not found'
        _usr = user.auth(password)
        assert _usr, 'invalid username or password'

        self.log(f"logged as {name}")

        return user

    @classmethod
    def mount(cls):
        default_root_password = 'root'

        _layer = cls()
        has_root = False
        for user in _layer.getOption('app.auth.users'):
            if user.name == 'root':
                has_root = True

            _layer.addUser(user)

        if has_root == False:
            _layer.addUser(User(
                    name = 'root',
                    # 2manywraps
                    password_hash = GetHash().implementation({'string': default_root_password}).items[0].value
                )
            )

        app.mount('AuthLayer', _layer)

    def getPermissions(self, likeness: ObjectPermission) -> Generator[ObjectPermission]:
        for item in self.getOption('app.auth.permissions'):
            if item.object_name != likeness.object_name:
                continue

            if item.user != likeness.user:# and item.user != None:
                continue

            if item.action != likeness.action:
                continue

            if item.allow != likeness.allow:
                continue

            yield item

    def compare_permissions(self, likeness: ObjectPermission):
        return len(list(app.AuthLayer.getPermissions(likeness))) > 0

    @classmethod
    def getSettings(cls):
        return [
            ListArgument(
                name = 'app.auth.users',
                default = [],
                orig = User
            ),
            ListArgument(
                name = 'app.auth.permissions',
                default = [],
                orig = ObjectPermission
            ),
            Argument(
                name = 'app.auth.every_call_permission_check',
                default = False,
                orig = Boolean
            )
        ]
