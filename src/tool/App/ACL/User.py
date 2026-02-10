from App.Objects.Object import Object
from App.ACL.Permissions.Permission import Permission
from App.ACL.Tokens.Token import Token, TokenExpiredError
from argon2 import PasswordHasher
from App import app
from typing import Optional
from pydantic import Field

class User(Object):
    name: str = Field()
    password_hash: str = Field(default = None, repr = False, exclude = True)
    inactive: bool = Field(default = False)
    via_token: Optional[Token] = Field(default = None)

    def auth(self, password: str) -> bool:
        hasher = PasswordHasher()

        if self.password_hash == None or hasher.verify(self.password_hash, password):
            return True

    def can(self, action: str, object: Object):
        if self.is_expired():
            raise TokenExpiredError('token expired')

        return Permission.check(Permission(
            object_name = object.getClassNameJoined(),
            user = self.name,
            action = action,
            allow = True
        ))

    def is_expired(self) -> bool:
        if self.via_token == None:
            return True

        return self.via_token.is_expired()

    def is_from_token(self) -> bool:
        return self.via_token != None
