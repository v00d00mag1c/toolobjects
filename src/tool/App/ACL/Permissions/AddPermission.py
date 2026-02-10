from App.Objects.Act import Act
from App.Objects.Arguments.Argument import Argument
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.ACL.Permissions.Permission import Permission

class AddPermission(Act):
    @classmethod
    def _arguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
            Argument(
                name = 'permission',
                orig = Permission
            )
        ])

    def implementation(self, i):
        pass
