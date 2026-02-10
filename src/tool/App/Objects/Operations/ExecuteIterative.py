from App.Objects.Test import Test
from App.Objects.Object import Object
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Argument import Argument
from App.Objects.Arguments.Assertions.NotNone import NotNone
from Data.Int import Int
from Data.Boolean import Boolean
from Data.Float import Float
from Data.String import String
from pydantic import Field
from App import app
import asyncio

class ExecuteIterative(Test):
    total_iterations: int = Field(default = 0)

    @classmethod
    def _arguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
            Argument(
                name = 'i_2',
                orig = Object,
                assertions = [NotNone()]
            ),
            Argument(
                name = 'start_iteration',
                orig = Int,
                default = 0
            ),
            Argument(
                name = 'interval',
                orig = Float,
                default = 10
            ),
            Argument(
                name = 'max_iterations',
                orig = Int,
                default = 5 # -1 for infinite
            ),
            Argument(
                name = 'same_all_time',
                orig = Boolean,
                default = False
            ),
            Argument(
                name = 'iteration_key',
                orig = String,
                default = 'iteration'
            )
        ])

    async def _implementation(self, i):
        _object = i.get('i_2')

        assert _object != None
        assert _object.canBeExecuted(), 'no execution interface'

        _obj = _object()

        _dict_args = i.getValues(exclude = [self._arguments().toNames()]).copy()

        reached_end = False

        is_stopped = False
        interval = i.get('interval')
        max_iterations = i.get('max_iterations')
        current_iterator = i.get('start_iteration')
        same_all_time = i.get('same_all_time')
        iteration_key = i.get('iteration_key')
        is_infinite = max_iterations < 1
        end_str = '∞'

        if is_infinite == False:
            end_str = max_iterations

        while reached_end == False and is_stopped == False:
            self.total_iterations += 1
            current_iterator += 1

            self.log(f"Run {current_iterator}/{end_str}, interval {interval}")

            _dict_args[iteration_key] = current_iterator

            if same_all_time == True:
                await _obj.execute(_dict_args)
            else:
                await _object().execute(_dict_args)

            if is_infinite == False:
                reached_end = current_iterator > max_iterations

            await asyncio.sleep(interval)
