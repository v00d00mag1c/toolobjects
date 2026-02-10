from App.Objects.Extractor import Extractor
from App.Objects.Arguments.Argument import Argument
from App.Objects.Arguments.Assertions.NotNoneAssertion import NotNoneAssertion
from Data.Int import Int
from App.Objects.Arguments.ArgumentDict import ArgumentDict
import random

class GetRandomInt(Extractor):
    @classmethod
    def _arguments(cls):
        return ArgumentDict(items=[
            Argument(
                name = "min",
                default = 0,
                orig = Int,
                assertions = [
                    NotNoneAssertion()
                ]
            ),
            Argument(
                name = "max",
                default = 100,
                orig = Int,
                assertions = [
                    NotNoneAssertion()
                ]
            )
        ])

    async def implementation(self, i) -> None:
        objects = Int()
        objects.value = self.randomInt(i.get('min'), i.get('max'))

        self.append(objects)

    def randomInt(self, min: int, max: int):
        return random.randint(min, max)

    def randomFloat(self, min: float, max: float):
        return random.uniform(min, max)
