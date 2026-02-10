from App.Objects.Object import Object
from App.Objects.Relations.LinkInsertion import LinkInsertion
from App.Storage.StorageUnit import StorageUnit
from typing import ClassVar
from pydantic import Field
from abc import abstractmethod
import ua_generator

class Webdriver(Object):
    webdriver_name: ClassVar[str] = 'none'
    platform: str = Field(default = None)
    file: LinkInsertion = Field(default = None)

    @abstractmethod
    async def start(self):
        ...

    def get_useragent(self) -> str:
        _passed = self.getOption('web.crawler.user_agent')
        if _passed == None:
            return ua_generator.generate(device='desktop', browser=['chrome', 'edge'])

        return _passed
