from pydantic import BaseModel
from typing import Callable

class Convertable(BaseModel):
    @classmethod
    def getConverters(cls) -> list:
        pass

    @classmethod
    def ignorePreviousConverters(cls) -> bool:
        return False

    @classmethod
    def getAllConverters(cls) -> list:
        _all = []

        for item in cls.getMRO():
            if hasattr(item, 'getConverters') == True:
                _list = item.getConverters()
                if _list == None:
                    continue

                for item in _list:
                    _all.append(item)

                if item.ignorePreviousConverters() == True:
                    break

        return _all

    @classmethod
    def findConvertationsForClass(cls, for_class: BaseModel) -> list:
        converters = []
        for item in cls.getAllConverters():
            if item.converts_to == for_class:
                converters.append(item)

        return converters

    async def convertTo(self, to_class: BaseModel):
        _itms = self.findConvertationsForClass(to_class)
        _conv = _itms[0]

        assert _conv != None, 'no convertation for this'

        _itm = _conv()
        return await _itm.execute(i = {'orig': self})
