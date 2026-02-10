from .Object import Object
from .Validable import Validable
from App.Executables.Call import Call
from App.Arguments.ArgumentsDict import ArgumentsDict
from App.Responses.Response import Response
from App.Objects.Variableable import Variableable
from typing import ClassVar
from pydantic import Field
import asyncio

class Executable(Variableable, Validable, Object):
    '''
    Object that has "execute()" interface, single entrypoint.
    
    getArguments(): validation
    '''

    self_name: ClassVar[str] = 'Executable'
    call: Call = Field(default = None)

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

        args = self.getAllArguments()
        passing = args.compareWith(
            inputs = i,
            check_arguments = check_arguments,
            raise_on_assertions = raise_on_assertions,
        )

        self.call = Call()
        self.call.predicate = self.meta.class_name_joined

        if hasattr(i, 'toOriginalDict') == False:
            self.call.arguments = i
        else:
            self.call.arguments = i.original_items

        await self.awaitTriggerHooks('before_execute', i = passing)

        response = await self.implementation_wrap(i = passing)

        # assert response != None, 'implementation() returned nothing'

        await self.awaitTriggerHooks('after_execute', i = passing)

        return response
