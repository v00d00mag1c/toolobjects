from Data.Primitives.Collections.Collection import Collection
from pydantic import Field

class List(Collection):
    media_types: list[str] = Field(default = [])
