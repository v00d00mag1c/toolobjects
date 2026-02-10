from .Object import Object
from .Mixins.Validable import Validable
from App.Objects.Arguments.ArgumentValues import ArgumentValues
from App.Objects.Responses.Response import Response
from App.Objects.Mixins.Variableable import Variableable
from App.Logger.LogPrefix import LogPrefix
from typing import ClassVar, Optional
from pydantic import Field
from App import app
from abc import abstractmethod
import asyncio

class Executable(Object, Variableable, Validable):
    id: int = 0
    self_name: ClassVar[str] = 'Executable'
    #internal_use: bool = Field(default = True)
    args: Optional[dict] = Field(default = {})
    _unserializable = ['id', 'variables', 'self_name']

    @classmethod
    def getClassEventTypes(cls) -> list:
        return ['before_execute', 'after_execute']

    @property
    def append_prefix(self) -> LogPrefix:
        return LogPrefix(
            id = self.id,
            #name = self.class_name
            name = 'ID'
        )

    @abstractmethod
    async def implementation(self, i: dict) -> Response:
        '''
        Entry point, must be overriden in your class
        '''
        ...

    async def implementation_wrap(self, i: dict) -> Response:
        '''
        another checks before implementation(). Can be overriden
        '''

        if asyncio.iscoroutinefunction(self.implementation):
            return await self.implementation(i)
        else:
            return self.implementation(i)

    async def execute(self, 
                      i: ArgumentValues | dict, 
                      check_arguments: bool = True, 
                      raise_on_assertions: bool = True,
                      skip_user_check: bool = False) -> Response:
        '''
        Internal method. Calls module-defined implementation() and returns what it returns
        '''

        self.id = app.app.executables_id.getIndex()
        if type(i) == dict:
            i = ArgumentValues(values = i)
        else:
            i.modified = True

        self.log(f"Calling {self.getClassNameJoined()}")

        if app.ExecutablesList != None:
            app.ExecutablesList.add(self)

        if app.AuthLayer.getOption('app.auth.every_call_permission_check') == True and skip_user_check == False:
            _name = ''
            _auth = i.get('auth', same=True)
            if _auth != None:
                _name = _auth.name

            assert self.canBeUsedBy(_auth), "access denied (executable={0}, every_call_permission_check=true, user={1})".format(self.getClassNameJoined(), _name)

        args = self.getAllArguments()
        vals = i.toDict()
        passing = args.compareWith(
            inputs = vals,
            check_arguments = check_arguments,
            raise_on_assertions = raise_on_assertions,
        )
        passing.check()

        await self.awaitTriggerHooks('before_execute', i = passing)

        response = await self.implementation_wrap(i = passing)

        # assert response != None, 'implementation() returned nothing'

        await self.awaitTriggerHooks('after_execute', i = passing)

        if app.ExecutablesList != None:
            app.ExecutablesList.remove(self)

        return response

    def integrate(self, args):
        '''
        Marks call as non-internal (as created by user).
        just sets args that can be flushed
        '''

        #self.internal_use = False # idk whats this
        self.args = args.values
