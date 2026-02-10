from App.Objects.Act import Act
from App.Arguments.ArgumentsDict import ArgumentsDict
from App.Arguments.Types.String import String
from App.Arguments.Assertions.NotNoneAssertion import NotNoneAssertion
from App.Responses.AnyResponse import AnyResponse
from pathlib import Path

from Files.File import File

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
        _item = File.fromPath(_path)

        return AnyResponse(
            data = _item.file.getContent()
        )
