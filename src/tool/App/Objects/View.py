from App.Objects.Executable import Executable
from typing import Any
from App.App import App
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Argument import Argument
from App.Objects.Arguments.Assertions.NotNone import NotNone

class View(Executable):
    '''
    Wrapper of the app. Contains executable interface that runs from tool.py
    '''

    app: Any = None

    def setApp(self, app: App) -> None:
        self.app = app

    def setAsCommon(self):
        '''
        Sets link that can be used as

        from App import app

        app.Logger.log(...)
        '''
        from App import app

        app.setView(self)

    def _implementation(self, i: dict = {}):
        pass

    def canUseObject(self, obj) -> bool:
        _allowed = obj.getAllowedViews()
        if _allowed == None:
            return True

        for item in _allowed:
            if item.getClassNameJoined() == self.getClassNameJoined():
                return True

    @classmethod
    def _arguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
            Argument(
                name = 'pre_i',
                orig = Executable,
                default = 'App.Objects.Operations.DefaultExecutorWheel',
                assertions = [
                    NotNone()
                ]
            ),
        ])
