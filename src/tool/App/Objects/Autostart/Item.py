from App.Objects.Object import Object
from App.Objects.Threads.ExecutionThread import ExecutionThread
from pydantic import Field
from App import app

class Item(Object):
    args: dict = Field(default = {})
    deactivated: bool = Field(default = False)

    def getArgs(self):
        return self.args

    def set_deactivated(self):
        self.deactivated = True

    def run(self, pre_i: Object, name: str = 'autostart_item', as_root: bool = False):
        _copied = self.args.copy()
        _copied['run_item'] = self
        if _copied.get('auth') == 'root' and as_root:
            _copied['auth'] = app.AuthLayer.getUserByName('root')
        else:
            _copied['auth'] = app.AuthLayer.byToken(_copied.get('auth'))

        thread = ExecutionThread(id = -1)
        thread.set_name(name)
        thread.set(pre_i.execute(_copied))
