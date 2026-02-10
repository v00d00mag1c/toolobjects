from App.Objects.Misc.Source import Source
from App.Objects.Mixins.Model import Model
from pydantic import Field
from typing import Literal, Optional

# It not logically extends Source, but the fields are almost similar so extending it
class Thumbnail(Source):
    role: Optional[list[Literal['image', 'video']]] = Field(default = [])
