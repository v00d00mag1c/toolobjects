from .Object import Object
from .Validable import Validable
from App.Arguments.ArgumentsDict import ArgumentsDict
from App.Responses.Response import Response
from App.Objects.Variableable import Variableable
from typing import ClassVar, Optional
from pydantic import Field
from App import app
import asyncio

class Executable(Object, Variableable, Validable):
    '''
    Object that has "execute()" interface, single entrypoint.
    
    getArguments(): validation

    common_object: another object that executable can represent
    '''

    id: int = 0
    self_name: ClassVar[str] = 'Executable'
    common_object: ClassVar[Optional[list]] = None

    @classmethod
    def getClassEventsTypes(cls) -> list:
        return ['before_execute', 'after_execute']

    async def implementation(self, i: ArgumentsDict) -> Response:
        '''
        Entry point, must be redefined in your class
        '''
        pass

    async def implementation_wrap(self, i: ArgumentsDict) -> Response:
        '''
        Wrap that can be overriden
        '''

        if asyncio.iscoroutinefunction(self.implementation):
            return await self.implementation(i)
        else:
            return self.implementation(i)

    async def execute(self, 
                      i: ArgumentsDict, 
                      check_arguments: bool = True, 
                      raise_on_assertions: bool = True) -> Response:
        '''
        Internal method. Calls module-defined implementation() and returns what it returns
        (No, it calls implementation_wrap())
        '''

        self.id = app.app.executables_id.getIndex()

        args = self.getAllArguments()
        passing = args.compareWith(
            inputs = i,
            check_arguments = check_arguments,
            raise_on_assertions = raise_on_assertions,
        )

        # TODO: provide single type
        #if type(i) == dict:
        #    self.args = i
        #else:
        #    self.args = i.toDict()

        await self.awaitTriggerHooks('before_execute', i = passing)

        response = await self.implementation_wrap(i = passing)

        # assert response != None, 'implementation() returned nothing'

        await self.awaitTriggerHooks('after_execute', i = passing)

        return response
