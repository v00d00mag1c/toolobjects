from App.Objects.Act import Act
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Argument import Argument
from App.Objects.Arguments.Assertions.NotNoneAssertion import NotNoneAssertion
from App.ACL.Acts.GetHash import GetHash
from App.ACL.User import User
from App import app

class CreateUser(Act):
    @classmethod
    def _arguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
            Argument(
                name = 'name',
                assertions = [NotNoneAssertion()]
            ),
            Argument(
                name = 'password',
                assertions = [NotNoneAssertion()]
            )
        ])

    async def implementation(self, i):
        _hash = GetHash().implementation({'string': i.get('password')})
        _user = User(name = i.get('name'), password_hash = _hash.items[0].value)

        app.AuthLayer.add_user(_user)
