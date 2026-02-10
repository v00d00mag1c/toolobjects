from App.Objects.Act import Act
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Argument import Argument
from App.Objects.Arguments.Assertions.NotNone import NotNone
from App.ACL.GetHash import GetHash
from App.ACL.User import User
from App import app

class CreateUser(Act):
    @classmethod
    def _arguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
            Argument(
                name = 'name',
                assertions = [NotNone()]
            ),
            Argument(
                name = 'password',
                assertions = [NotNone()]
            )
        ])

    async def _implementation(self, i):
        _hash = GetHash()._implementation({'string': i.get('password')})
        _user = User(name = i.get('name'), password_hash = _hash.items[0].value)

        app.AuthLayer.add_user(_user)
