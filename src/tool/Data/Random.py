from App.Objects.Extractor import Extractor
from App.Arguments.Types.Int import Int
from App.Arguments.Assertions.NotNoneAssertion import NotNoneAssertion
from Data.Number import Number
from App.Arguments.ArgumentDict import ArgumentDict
import random

class Random(Extractor):
    @classmethod
    def getArguments(cls):
        return ArgumentDict(items=[
            Int(
                name = "min",
                default = 0,
                assertions = [
                    NotNoneAssertion()
                ]
            ),
            Int(
                name = "max",
                default = 100,
                assertions = [
                    NotNoneAssertion()
                ]
            )
        ])

    async def implementation(self, i) -> None:
        objects = Number()
        objects.number = self.randomInt(i.get('min'), i.get('max'))

        self.append(objects)

    def randomInt(self, min: int, max: int):
        return random.randint(min, max)

    def randomFloat(self, min: float, max: float):
        return random.uniform(min, max)
