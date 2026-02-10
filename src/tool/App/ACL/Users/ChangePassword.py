from App.Objects.Act import Act
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Argument import Argument
from App.Objects.Arguments.Assertions.NotNone import NotNone
from Data.Types.String import String
from App.ACL.GetHash import GetHash

class ChangePassword(Act):
    @classmethod
    def _arguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
            Argument(
                name = 'new',
                orig = String,
                assertions = [NotNone()],
            ),
            Argument(
                name = 'auth',
                assertions = [NotNone()],
            )
        ])

    async def _implementation(self, i):
        user = i.get('auth')
        _hash = GetHash()._implementation({'string': i.get('new')})

        user.password_hash = _hash.items[0].value
        user.save()

        self.log('password was changed')
