from Data.Primitives.Collections.Collection import Collection
from pydantic import Field
from App.Objects.Operations.Create.CreationItem import CreationItem

class List(Collection):
    media_types: list[str] = Field(default = [])

    @classmethod
    def _creations(cls) -> list:
        return [
            CreationItem(
                name = 'Gallery',
                object_name = 'Media.List',
                create = 'Media.List.Create'
            ),
        ]
