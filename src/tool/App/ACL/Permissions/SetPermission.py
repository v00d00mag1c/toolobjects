from App.Objects.Act import Act
from App.Objects.Arguments.Argument import Argument
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.ACL.Permissions.ObjectPermission import ObjectPermission

class SetPermission(Act):
    @classmethod
    def getArguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
            Argument(
                name = 'permission',
                orig = ObjectPermission
            )
        ])

    def implementation(self, i):
        pass
