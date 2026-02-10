from App.Objects.Object import Object
from pydantic import Field

class User(Object):
    name: str = Field()
    password_hash: str = Field()
