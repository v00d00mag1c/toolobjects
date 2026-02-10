from App.Objects.Object import Object
from App.Objects.Relations.LinkInsertion import LinkInsertion
from App.Storage.StorageUnit import StorageUnit
from Web.HTTP.UserAgent import UserAgent
from typing import ClassVar
from pydantic import Field
from abc import abstractmethod

class Webdriver(Object):
    webdriver_name: ClassVar[str] = 'none'
    platform: str = Field(default = None)
    file: LinkInsertion = Field(default = None)

    @abstractmethod
    async def start(self, i):
        ...

    def get_useragent(self) -> str:
        _passed = self.getOption('web.crawler.user_agent')
        if _passed == None:
            return UserAgent.generate()

        return _passed
