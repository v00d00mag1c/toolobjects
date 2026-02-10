from App.Objects.Object import Object
from pydantic import Field
from App.ACL.User import User
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
        assert user.auth(password), 'invalid username or password'

        self.log(f"logged as {name}")

    @classmethod
    def mount(cls):
        _layer = cls()
        _users = [
            User(
                name = 'root',
                password_hash = '123'
            )
        ]

        for user in _users:
            _layer.addUser(user)

        app.mount('AuthLayer', _layer)
