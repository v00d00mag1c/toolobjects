from App.Objects.Object import Object
from App.ACL.User import User
from App.Objects.Responses.Responses import Responses
from App.Objects.Queue.Item import Item
from App.Objects.Queue.OutputItem import OutputItem
from App.Objects.Operations.DefaultExecutorWheel import DefaultExecutorWheel
from App.Objects.Misc.Increment import Increment
from pydantic import Field

class Queue(Object):
    '''
    Class that allows to run multiple executables with his context

    Uses App.Objects.Queue.Item for "prestart" and "items".

    prestart - Items that will be executed before the "items". You can pass variables there. Things that does not has "execute()"
    items - Items that will be executed as main process
    output - Queue output format

    You can reference results by "$" for prestart and "#" for items
    '''

    prestart: list[Item] = []
    items: list[Item] = []
    output: list[OutputItem] = []
    repeat: int = Field(default = 1)
    return_index: int = Field(default = None)

    async def run(self, auth: User):
        _prestart = list()
        _items = list()

        responses = Responses()
        iterator = Increment()

        for prestart_item in self.prestart:
            _item = prestart_item.get_predicate()
            _prestart.append(_item(**prestart_item.get_build_arguments(_prestart, _items)))

        _wheel = DefaultExecutorWheel()

        for iter in range(0, self.repeat):
            if self.repeat > 1:
                self.log('cycle {0}'.format(iter))

            for item in self.items:
                item.id = iterator.getCount()

                try:
                    _items.append(await item.run(_prestart, _items, _wheel, auth))
                except Exception as e:
                    self.log_error(e, exception_prefix='queue item {0} caused error: '.format(item.id))
                    self.fatal(e)

                iterator.increment()

        for out_class in self.output:
            responses.append(out_class.apply(_prestart, _items))

        if self.return_index != None:
            return responses.responses[self.return_index]

        return responses
