from App.Objects.Act import Act
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Argument import Argument
from App.Objects.Arguments.Assertions.NotNone import NotNone
from App.Objects.Responses.ObjectsList import ObjectsList
from App.ACL.Tokens.Token import Token
from Data.Types.String import String
from Data.Types.Boolean import Boolean
from App import app
import datetime

class Get(Act):
    @classmethod
    def _arguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
            Argument(
                name = 'username',
                orig = String,
                assertions = [NotNone()]
            ),
            Argument(
                name = 'password',
                orig = String,
                assertions = [NotNone()]
            ),
            Argument(
                name = 'infinite',
                orig = Boolean,
                default = False
            )
        ])

    def _implementation(self, i):
        _user = app.AuthLayer.login(
            name = i.get('username'),
            password = i.get('password')
        )

        _token = Token(
            value = Token.get_hash(),
            user = _user.name,
            expires_at = Token.get_expired()
        )
        if i.get('infinite'):
            _token.infinite = True

        _token.flush(app.Storage.get('users'))

        return ObjectsList(items = [String(value = _token.value)], unsaveable = True)

    @classmethod
    def canBeUsedBy(cls, user):
        return True
        #return user.name == 'root' or user == None
