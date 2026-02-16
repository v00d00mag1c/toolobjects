from Web.URL import URL as OldURL
from Web.Pages.Assets.Asset import Asset
from pydantic import Field

class URL(OldURL, Asset):
    value: str = Field(default = None)
    target: str = Field(default = None)
    label: str = Field(default = None)
    is_download: bool = Field(default = False)
    is_protocol: bool = Field(default = False)

    def set_url(self, href: str, base_url: str = ''):
        if not href.startswith('http'):
            href = base_url + '/' + href

        self.value = href

    def set_protocol(self, url: str):
        self.value = url
        self.is_protocol = True

    def get_url(self):
        return self.value
