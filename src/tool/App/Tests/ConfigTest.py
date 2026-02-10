from App.Objects.Test import Test
from App import app

class ConfigTest(Test):
    async def implementation(self, i):
        self.log('running test!')

        val_test = app.Config.get("test")
        self.log(f"the key with name 'test' is {val_test}")
        self.log(f"changing 'test' value to 121212")

        app.Config.set("test", "121212")
        val_test_2 = app.Config.get("test")
        self.log(f"the key with name 'test' is now {val_test_2}")

        self.log(f"updating compare of config")
        #app.Config.updateCompare()

        self.log(f"all the settings of config: {app.Config.values.compare}")
        self.log(f"env:")

        env_test = app.Env.get("test")
        self.log(f"env test is {env_test}")

        app.Env.set("test", "676767")
        env_test_2 = app.Env.get("test")
        self.log(f"env test is {env_test_2}")
