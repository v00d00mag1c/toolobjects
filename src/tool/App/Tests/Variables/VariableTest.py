from App.Objects.Test import Test
from App.Tests.Variables.ExtractorTest import ExtractorTest

class VariableTest(Test):
    async def _implementation(self, i):
        def _test(variable):
            self.log_success("UPDATE {0}".format(variable.name))

        _test_ex = ExtractorTest()
        _test_ex.addHook('var_update', _test)

        return await _test_ex.execute({})
