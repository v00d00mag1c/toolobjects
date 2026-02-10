from App.Objects.Object import Object
from App.ACL.Permissions.Permission import Permission
from argon2 import PasswordHasher
from App import app
from pydantic import Field

class User(Object):
    name: str = Field()
    password_hash: str = Field(default = None, repr = False, exclude = True)
    inactive: bool = Field(default = False)

    def auth(self, password: str) -> bool:
        hasher = PasswordHasher()

        if self.password_hash == None or hasher.verify(self.password_hash, password):
            return True

    def can(self, action: str, object: Object):
        # ???
        return Permission.check(Permission.getPermissions(Permission(
            object_name = object.getClassNameJoined(),
            user = self.name,
            action = action,
            allow = True
        )))
