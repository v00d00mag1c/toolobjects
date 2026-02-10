from App.Objects.Test import Test
from Media.Text.Text import Text
from Data.Random.GetRandomInt import GetRandomInt
from App import app

class FlushTest(Test):
    async def implementation(self, i):
        self.log('creating models')
        _id = GetRandomInt().randomInt(0,1)

        items = [Text(value='123456'),Text(value='asdfghjkl')]

        _storage = app.Storage.get('tmp')
        _item = items[_id].flush(_storage)

        self.log(f'we saved object {_id} to id {_item.uuid}')
        self.log(f'getting object from db item')

        self.log_raw(_item.toPython())
        self.log_raw(_item.toPython().to_json())

        _lnked = Text(value='888')
        #_lnked.flush(_storage)

        try:
            _item.toPython().link(_lnked, role = ['internal'])
        except AssertionError as e:
            self.log('assertion error so item not saved')
            raise e
