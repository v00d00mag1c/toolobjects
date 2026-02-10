from Data.Primitives.Collections.Collection import Collection
from App.Objects.Relations.LinkInsertion import LinkInsertion
from Media.Images.Image import Image
from pydantic import Field

class Album(Collection):
    cover: LinkInsertion | Image = Field(default = None)
