from pydantic import BaseModel

class Convertable(BaseModel):
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

    def displayAsString(self, show_id: bool = True) -> str:
        def getIdSign():
            if self.hasDb():
                return f"[{self._db._adapter._storage_item.name}_{self._db.uuid}]"

            return ''
    
        _ret = "<{0}>".format(self._getClassNameJoined()) # self.__repr_str__(', ')
        _res = self._display_as_string()
        if _res != None:
            _ret = _res

        if show_id == True:
            _ret += getIdSign()

        return _ret

    def _display_as_string(self) -> str:
        return self.any_name
