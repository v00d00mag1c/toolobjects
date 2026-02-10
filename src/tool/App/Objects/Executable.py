from .Object import Object
from .Mixins.Validable import Validable
from App.Objects.Arguments.ArgumentValues import ArgumentValues
from App.Objects.Responses.Response import Response
from App.Objects.Responses.NoneResponse import NoneResponse
from App.Objects.Mixins.Variableable import Variableable
from App.Objects.Threads.ExecutionThread import ExecutionThread
from App.Logger.LogPrefix import LogPrefix
from typing import ClassVar, Optional
from pydantic import Field
from App import app
from abc import abstractmethod
import asyncio

class Executable(Object, Variableable, Validable):
    id: int = 0
    self_name: ClassVar[str] = 'Executable'
    thread: Optional[ExecutionThread] = Field(default = None)
    args: Optional[dict] = Field(default = {})

    _unserializable = ['id', 'variables', 'self_name', 'event_index']

    @classmethod
    def getClassEventTypes(cls) -> list:
        return ['before_execute', 'after_execute']

    @property
    def append_prefix(self) -> LogPrefix:
        return LogPrefix(
            id = self.id,
            name = 'ID'
        )

    @abstractmethod
    async def _implementation(self, i: dict) -> Response:
        '''
        Entry point, must be overriden in your class
        '''
        ...

    async def implementation_wrap(self, i: dict) -> Response:
        '''
        another checks before _implementation(). Can be overriden
        '''

        if asyncio.iscoroutinefunction(self._implementation):
            return await self._implementation(i)
        else:
            return self._implementation(i)

    async def execute(self, 
                      i: ArgumentValues | dict = {}, 
                      check_arguments: bool = True, 
                      raise_on_assertions: bool = True,
                      skip_user_check: bool = False) -> Response:
        '''
        Internal method. Calls module-defined _implementation() and returns what it returns
        '''

        self.id = app.app.executables_id.getIndex()
        if type(i) == dict:
            i = ArgumentValues(values = i)
        else:
            i.modified = True

        self.log("args: {0}".format(i.getPlaceholderValues()), role = ['executable.call'])

        if skip_user_check == False:
            if app.AuthLayer.getOption('app.auth.every_call_permission_check') == True:
                _name = ''
                _auth = i.get('auth', same=True)
                if _auth != None:
                    _name = _auth.name

                assert self.canBeUsedBy(_auth), "access denied (executable={0}, every_call_permission_check=true, user={1})".format(self._getClassNameJoined(), _name)

        passing = self._compare(i.toDict(), check_arguments = check_arguments, raise_on_assertions = raise_on_assertions)

        await self.awaitTriggerHooks('before_execute', i = passing)

        response = await self.implementation_wrap(i = passing)

        # assert response != None, '_implementation() returned nothing'

        await self.awaitTriggerHooks('after_execute', i = passing)

        if response == None:
            return NoneResponse()

        return response

    def _compare(self, vals, check_arguments: bool = True, raise_on_assertions: bool = True, check_assertions: bool = True):
        args = self.getArguments()
        values = args.compareWith(
            inputs = vals,
            check_arguments = check_arguments,
            raise_on_assertions = raise_on_assertions,
        )

        if check_assertions:
            values.check()

        return values

    def integrate(self, args):
        '''
        Marks call as non-internal (as created by user).
        just sets args that can be flushed
        '''

        #self.internal_use = False # idk whats this
        self.args = args.values
