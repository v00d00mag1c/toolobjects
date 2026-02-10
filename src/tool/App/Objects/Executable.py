from .Object import Object
from App.Arguments.ArgumentsDict import ArgumentsDict
from App.Responses.Response import Response

class Executable(Object):
    class _Hooks(Object._Hooks):
        @property
        def events(self) -> list:
            return ('before_execute', 'after_execute')

    @classmethod
    def getArguments(cls) -> ArgumentsDict:
        return ArgumentsDict(items = {})

    def getRecursiveArguments(self) -> ArgumentsDict:
        '''
        Joins ArgumentDicts from all extended classes
        '''

        # Takes current ArgumentsDict cuz it can contain properties
        _list = self.getArguments()

        # Slicing 1 because first arguments already got
        for _class in self.meta.mro[1:]:
            if hasattr(_class, 'getArguments') == True:
                new_arguments = _class.getArguments()
                if new_arguments == None:
                    continue

                _list.join(new_arguments)

        return _list

    async def implementation(self, i: ArgumentsDict) -> Response:
        '''
        Entry point, must be redefined in your class
        '''
        pass

    async def implementation_wrap(self, i: ArgumentsDict) -> Response:
        return await self.implementation(i)

    async def execute(self, 
                      i: ArgumentsDict, 
                      check_arguments: bool = True, 
                      raise_on_assertions: bool = True) -> Response:
        '''
        Internal method. Calls module-defined implementation() and returns what it returns
        (No, it calls implementation_wrap())
        '''

        args = self.getRecursiveArguments()
        passing = args.compareWith(
            inputs = i,
            check_arguments = check_arguments,
            raise_on_assertions = raise_on_assertions,
        )

        await self.hooks.await_trigger('before_execute', i = passing)

        response = await self.implementation_wrap(i = passing)

        await self.hooks.await_trigger('after_execute', i = passing)

        return response
