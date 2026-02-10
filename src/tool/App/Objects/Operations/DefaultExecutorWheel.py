from App.Objects.Act import Act
from App.Arguments.ArgumentDict import ArgumentDict
from App.Arguments.Objects.Executable import Executable
from App.Arguments.Types.String import String
from App.Arguments.Assertions.NotNoneAssertion import NotNoneAssertion
from App.Arguments.Assertions.InputNotInValues import InputNotInValues
from App.Arguments.ArgumentValues import ArgumentValues
from App.Responses.ObjectsList import ObjectsList
from App.Storage.Movement.Save import Save
from App import app

class DefaultExecutorWheel(Act):
    '''
    Class that switches the action looking by object type
    '''

    async def implementation(self, i: ArgumentValues):
        executable = i.get('i')
        assert executable != None, 'not found object'
        assert executable.canBeExecuted(), 'object does not contains execute interface'
        assert app.app.view.canUseObject(executable), 'object cannot be used at this view'
        assert executable.canBeUsedBy(None), 'access denied'

        _item = executable()
        _item.integrate(i.values)
        results = await _item.execute(i = i)

        if isinstance(results, ObjectsList):
            save_to = i.get('save_to')

            if save_to != None:
                _save = Save()
                await _save.execute({
                    'items': results,
                    'storage': save_to
                })

        return results

    @classmethod
    def getArguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
            Executable(
                name = 'i',
                default = 'App.Queue.Run',
                assertions = [
                    NotNoneAssertion(),
                    InputNotInValues(values=['App.Console.ConsoleView', 'App.Console.ConsoleView.ConsoleView'])
                ]
            ),
            String(
                # Save to
                name = 'save_to',
                default = None,
            )
        ],
        missing_args_inclusion = True)
