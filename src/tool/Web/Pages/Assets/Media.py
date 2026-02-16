from Web.Pages.Assets.Asset import Asset
from pydantic import Field

class Media(Asset):
    tagName: str = Field(default = None)
    alt: str = Field(default = None)
