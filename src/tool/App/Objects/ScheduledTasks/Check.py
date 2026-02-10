from App.Objects.Act import Act
from App import app
from datetime import datetime, timezone
from App.Objects.Threads.ExecutionThread import ExecutionThread
from App.Objects.Operations.DefaultExecutorWheel import DefaultExecutorWheel
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Argument import Argument
from Data.Types.Boolean import Boolean

class Check(Act):
    @classmethod
    def _arguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
            Argument(
                name = 'delete_after',
                orig = Boolean,
                default = True
            )
        ])

    async def _implementation(self, i):
        query = app.Storage.get('scheduled_tasks').adapter.getQuery()
        items = query.toObjectsList()

        # self.log('totally {0} tasks'.format(items.getCount()))

        now = datetime.now(timezone.utc)
        pre_i = DefaultExecutorWheel()
        _iterator = 0

        for task in items.getItems():
            if task.deactivated == True:
                self.log('task {0} is deactivated'.format(task.getDbIds()), role = ['scheduled_tasks', 'scheduled_tasks.deactivated'])
                continue

            if task.run_at >= now or task.deactivated == True:
                self.log('task {0} will be run after {1}s'.format(task.getDbIds(), round(task.run_at.timestamp() - now.timestamp(), 2)), role = ['scheduled_tasks'])
    
                continue

            try:
                self.log('time for {0} ({1})'.format(task.getDbIds(), task.run_at), role = ['scheduled_tasks'])

                if i.get('delete_after'):
                    task.delete(commit = True)

                    self.log('task {0} is deleted'.format(task.getDbIds()), role = ['scheduled_tasks', 'scheduled_tasks.deleted'])

                task.run(pre_i, 'scheduled_item ' + str(_iterator), self.getOption('app.scheduled_tasks.as_root'))

                _iterator += 1

                self.log('task {0} is succeed'.format(task.getDbIds()), role = ['scheduled_tasks'])
            except Exception as e:
                self.log_error(e)

                # Error occured, but not deleting the task
                task.set_deactivated()
                task.end()

                continue
