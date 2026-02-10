from App.Executables.Act import Act
from App.Arguments.ArgumentsDict import ArgumentsDict
from App.Arguments.Types.String import String
from App.Arguments.Assertions.NotNoneAssertion import NotNoneAssertion
from App.Responses.AnyResponse import AnyResponse
from pathlib import Path

from Files.File import File
from Files.Dir import Dir

class Navigate(Act):
    @classmethod
    def getArguments(cls) -> ArgumentsDict:
        return ArgumentsDict.fromList([
            String(
                name = 'path',
                assertions = [
                    NotNoneAssertion()
                ]
            )
        ])

    async def implementation(self, i):
        _path = Path(str(i.get('path')))
        _item = None

        if _path.is_dir() == True:
            _item = Dir(
                path = _path.as_posix()
            )
        else:
            _item = File(
                path = _path.as_posix()
            )

        return AnyResponse(
            data = _item.getContent()
        )
