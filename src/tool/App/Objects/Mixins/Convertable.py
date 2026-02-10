from pydantic import BaseModel
from typing import Any, Callable, Generator

class Convertable(BaseModel):
    '''
    Convertable and Displayable
    '''

    @classmethod
    def findConvertationsForClass(cls, for_class: BaseModel) -> list:
        converters = []
        for submodule in cls.getSubmodules(with_role=['convertation']):
            object_out = submodule.item.getSubmodules(with_role=['object_out'])
            for _submodule in object_out:
                if _submodule.item.isSame(for_class):
                    converters.append(submodule)

        return converters

    async def convertTo(self, to_class: BaseModel):
        _itms = self.findConvertationsForClass(to_class)
        _conv = _itms[0]

        assert _conv != None, 'no convertation for this'

        _itm = _conv.item()
        return await _itm.execute(i = {'orig': self})

    @classmethod
    def _displayments(cls) -> list[BaseModel]:
        return None

    @classmethod
    def getDisplayments(cls) -> Generator[BaseModel]:
        for item in cls.getMRO():
            if hasattr(item, '_displayments') == True:
                new = item._displayments()
                if new == None:
                    continue

                for item in new:
                    yield item

    def displayAs(self, as_type: str = 'str') -> str | Any:
        # It would'nt work with JSComponentDisplayment (change later)
        for displayment_probaly in self.getDisplayments():
            if as_type in displayment_probaly.display_type:
                return displayment_probaly.value().implementation(i = {'orig': self})

    def displayAsString(self, show_id: bool = True) -> str:
        def getIdSign():
            if self.hasDb():
                return f"[{self._db._adapter._storage_item.name}_{self._db.uuid}]"

            return '[not flushed]'
    
        _ret = "<{0}>".format(self.getClassNameJoined()) # self.__repr_str__(', ')
        _res = self.displayAs(as_type = 'str')
        if _res != None:
            _ret = _res

        if show_id == True:
            _ret += getIdSign()

        return _ret
