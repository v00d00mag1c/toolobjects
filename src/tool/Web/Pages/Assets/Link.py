from Web.Pages.Assets.Asset import Asset
from pydantic import Field

class Link(Asset):
    rel: list[str] = Field(default = [])
    media: str = Field(default = None)
    type: str = Field(default = None)
    as_item: str = Field(default = None, alias = 'as')

    def should_download(self):
        if self.type == None and self.as_item == None and self.rel == None:
            return False

        is_internal = True
        for key in ['icon', 'stylesheet']:
            if key in self.rel:
                is_internal = False

        if is_internal == True:
            return False

        return True
