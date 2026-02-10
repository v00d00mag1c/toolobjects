from App.Objects.Executable import Executable
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Assertions.NotNoneAssertion import NotNoneAssertion
from App.Objects.Arguments.Argument import Argument
from App.Logger.Log import Log
from App import app

class PrintLog(Executable):
    @classmethod
    def getArguments(cls):
        return ArgumentDict(items=[
            Argument(
                name = 'log',
                orig = Log,
                assertions = [NotNoneAssertion()]
            )
        ])

    def implementation(self, i):
        self.log_raw(Log.toStr(i.get('log').toParts(
            show_time = app.Config.get('logger.print.console.show_time'),
            show_role = app.Config.get('logger.print.console.show_role')
        )))
