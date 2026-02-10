### Scheduled tasks

Scheduled tasks are stored in storage `scheduled_tasks`. The "Task" object is the same as autostart object but contains time when it should run (`run_at`).

It can be created manually, maybe... via:

```
python tool.py -i App.Objects.ScheduledTasks.Task -force_flush 1 -save_to common

python tool.py -i App.Objects.ScheduledTasks.Add -task [got id]
```

Then available tasks can be checked via `App.Objects.ScheduledTasks.Check`. This executable should be added in [autostart](./autostart.md), by the way. After, or more correctly, before, the completion the task will be deleted.
