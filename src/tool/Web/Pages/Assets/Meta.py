from Web.Pages.Assets.Asset import Asset
from pydantic import Field
from typing import Optional

class Meta(Asset):
    name: Optional[str] = Field(default = None)
    content: Optional[str] = Field(default = None)
    property: Optional[str] = Field(default = None)

    def get_name(self) -> str:
        return self.name

    def get_content(self) -> str:
        if self.content == None:
            return self.property

        return self.content

    def get_any_name(self):
        if self.name:
            return self.name

        if self.property:
            return self.property

    async def download_function(self, dir):
        pass
