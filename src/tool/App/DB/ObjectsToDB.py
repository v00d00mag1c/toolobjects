from App.Objects.Executable import Executable
from App.Arguments.ArgumentsDict import ArgumentsDict
from App.Arguments.Objects.List import List

class ObjectsToDB(Executable):
    @classmethod
    def getArguments(cls):
        return ArgumentsDict.fromList([
            List(
                name = 'models'
            )
        ])
