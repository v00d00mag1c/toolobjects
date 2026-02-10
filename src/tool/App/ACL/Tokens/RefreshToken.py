from App.Objects.Act import Act
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Argument import Argument
from App.Objects.Arguments.Assertions.NotNone import NotNone
from App.ACL.Tokens.Token import Token
from Data.Types.String import String
from App.DB.Query.Condition import Condition
from App.DB.Query.Values.Value import Value
from App import app
from App.Objects.Responses.ObjectsList import ObjectsList

class RefreshToken(Act):
    @classmethod
    def _arguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
            Argument(
                name = 'token',
                orig = String,
                assertions = [NotNone()]
            )
        ])

    def _implementation(self, i):
        _token = i.get('token')
        _tokens = app.Storage.get('users').adapter.getQuery()
        _tokens.where_object(Token)
        _tokens.addCondition(Condition(
            val1 = Value(
                column = 'content',
                json_fields = ['value'],
            ),
            operator = '==',
            val2 = Value(
                value = _token
            )
        ))
        _item = _tokens.first()

        assert _item != None, 'invalid token'

        token = _item.toPython()

        assert token.can_be_refreshed(), "token can't be refreshed"

        new_token = Token(
            value = Token.get_hash(),
            user = token.user,
            expires_at = Token.get_expired()
        )
        new_token.flush(app.Storage.get('users'))
        new_token.save()

        token.delete()

        return ObjectsList(items = [String(value = new_token.value)], unsaveable = True)
