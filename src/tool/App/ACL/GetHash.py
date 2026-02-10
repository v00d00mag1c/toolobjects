from App.Objects.Act import Act
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Argument import Argument
from App.Objects.Arguments.Assertions.NotNone import NotNone
from App.Objects.Responses.ObjectsList import ObjectsList
from argon2 import PasswordHasher
from Data.Types.String import String

class GetHash(Act):
    @classmethod
    def _arguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
            Argument(
                name = 'string',
                orig = String,
                assertions = [NotNone()]
            )
        ])

    def _implementation(self, i):
        hasher = PasswordHasher()

        return ObjectsList(items = [String(value = hasher.hash(i.get('string')))])
