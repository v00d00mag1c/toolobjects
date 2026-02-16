from App.Objects.Object import Object
from App.ACL.Permissions.Permission import Permission
from App.ACL.Tokens.Token import Token, TokenExpiredError
from argon2 import PasswordHasher
from App import app
from typing import Optional
from pydantic import Field

class User(Object):
    name: str = Field()
    password_hash: str = Field(repr = False)
    inactive: bool = Field(default = False)
    via_token: Optional[Token] = Field(default = None)
    permissions: list[str] = Field(default = [])

    def auth(self, password: str) -> bool:
        hasher = PasswordHasher()
        if self.password_hash == None or hasher.verify(self.password_hash, password):
            return True

    def can(self, action: str, object: Object):
        if self.is_expired():
            raise TokenExpiredError('token expired')

        return Permission.check(Permission(
            object_name = object._getClassNameJoined(),
            user = self.name,
            action = action,
            allow = True
        ))

    def has_permission(self, name: str):
        if self.name == 'root':
            return True

        return name in self.permissions

    def is_expired(self) -> bool:
        if self.via_token == None:
            return True

        return self.via_token.is_expired()

    def is_from_token(self) -> bool:
        return self.via_token != None
