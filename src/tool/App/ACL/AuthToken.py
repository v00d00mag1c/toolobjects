from App.Objects.Object import Object
from pydantic import Field

class AuthToken(Object):
    string: str = Field()
