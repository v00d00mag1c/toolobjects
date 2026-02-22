from App.Objects.Object import Object
from datetime import datetime
from pydantic import Field
import secrets
from App import app

class TokenExpiredError(Exception):
    pass

class Token(Object):
    value: str = Field()
    user: str = Field()
    expires_at: datetime = Field()
    infinite: bool = Field(default = False)

    _unserializable_on_output = ['value']

    @classmethod
    def isEditable(cls) -> bool:
        return False

    def is_expired(self):
        if self.infinite == True:
            return False

        return datetime.now().timestamp() > self.expires_at.timestamp()

    def can_be_refreshed(self):
        return app.AuthLayer.getOption('app.auth.token.refresh_limit') + datetime.now().timestamp() > self.expires_at.timestamp()

    @staticmethod
    def get_hash():
        return secrets.token_urlsafe(64)

    @staticmethod
    def get_expired(lifetime: int = None):
        if lifetime == None:
            lifetime = app.AuthLayer.getOption('app.auth.token.life')

        assert lifetime > 0, 'Invalid token lifetime'

        _now = datetime.now().timestamp()
        return _now + lifetime

    def to_user(self) -> Object:
        _user = app.AuthLayer.getUserByName(self.user)
        if _user != None:
            _user.via_token = self

        return _user
