from App.Objects.Act import Act
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Argument import Argument
from App.Objects.Arguments.Assertions.NotNone import NotNone
from Data.String import String
from App import app
from App.DB.Query.Condition import Condition
from App.ACL.Tokens.Token import Token

class Reset(Act):
    @classmethod
    def _arguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
            Argument(
                name = 'user',
                orig = String,
                assertions = [NotNone()]
            ),
        ])

    def _implementation(self, i):
        user = i.get('user')
        _user = app.AuthLayer.getUserByName(user)

        assert _user != None, 'user not found'

        _tokens = app.Storage.get('users').adapter.getQuery()
        _tokens.where_object(Token)
        _tokens.addCondition(Condition(
            val1 = 'content',
            json_fields = ['user'],
            operator = '==',
            val2 = _user.name
        ))

        for item in _tokens.getAll():
            token = item.toPython()
            token.delete()
