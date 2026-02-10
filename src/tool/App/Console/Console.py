from App.Views.View import View
from App.Arguments.ArgumentsDict import ArgumentsDict
from App.Data.DictList import DictList
from App.Arguments.Assertions.NotNoneAssertion import NotNoneAssertion
from App.Arguments.Assertions.InputNotInValues import InputNotInValues
from App.Arguments.Objects.Executable import Executable
from App.Logger.Log import Log
from Data.JSON import JSON

class Console(View):
    '''
    View that represents CMD. Runs executable from "i"
    '''

    async def implementation(self, i: dict = {}):
        executable = i.get('i')
        assert executable.meta.can_be_executed, 'cannot be executed'
        results = await executable().execute(i = i)

        if results == None:
            self.log('nothing returned')
        else:
            _json = JSON(data = results.to_json())
            print(_json.dump(indent = 4))

    @classmethod
    def getArguments(cls) -> ArgumentsDict:
        dicts = ArgumentsDict.fromList([
            Executable(
                name = 'i',
                default = 'App.Queue.Run.Run',
                assertions = [
                    NotNoneAssertion(),
                    InputNotInValues(values=['App.Console.Console.Console'])
                ]
            )
        ])
        dicts.missing_args_inclusion = True

        return dicts
