from App.Objects.Act import Act
from App.Objects.Arguments.Argument import Argument
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.ACL.Permissions.Permission import Permission
from App import app

class AddPermission(Act):
    @classmethod
    def _arguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
            Argument(
                name = 'permission',
                orig = Permission
            )
        ])

    def _implementation(self, i):
        app.AuthLayer.add_permission(i.get('permission'))
