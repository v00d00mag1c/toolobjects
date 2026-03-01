### Installation

You should have installed python, pip in your system, and python should be available in %PATH%.

1. Download ZIP of this repository and extract it somewhere or do git clone.
2. CD to the extracted folder, then cd to `src`
3. Create a Python Virtual Environment using the script:

powershell:

```bash
.\venv.ps1
```

bash:

```bash
.\venv.sh
```

4. Install the common requirements, using

```bash
pip install -e .
```

or

```bash
.\update.ps1
```

5. cd into "tool"
6. Now you need to install all external requirements:

```bash
python tool.py -i App.Objects.Requirements.InstallEvery
```

7. You need to change root's password:

```
python tool.py -i App.ACL.Users.ChangePassword -new [new password]
```

8. Create `config.json` in `src/config` if not exists, set the content:
```
{
    "app.autostart.as_root": true,
    "app.scheduled_tasks.as_root": true,
    "app.autostart.items": [
        {
            "args": {
                "i": "App.Objects.Operations.ExecuteIterative",
                "i_2": "App.Objects.ScheduledTasks.Check",
                "max_iterations": -1,
                "auth": "root"
            }
        }
    ],
    "logger.print.exclude": [
        {
            "role": ["scheduled_tasks.deactivated"]
        },
        {
            "role": ["objects.loading"]
        },
        {
            "role": ["console.print.returned.nothing"]
        },
        {
            "section": ["App.Console.Console"]
        },
        {
            "role": ["auth.console"]
        },
        {
            "section": ["App.Objects.Operations.DefaultExecutorWheel"]
        },
        {
            "role": ["storage.item"]
        },
        {
            "role": ["thread"]
        },
        {
            "role": ["executable.call"]
        },
        {
            "role": ["asset_request"]
        },
        {
            "role": ["displayment_client_request"]
        }
    ]
}
```

9. Pass the name of one of the items below as `-view`:

- [App.Console](../objects/App.Console.Console.md)
- [App.Console.Interactive](../objects/App.Console.Interactive.Interactive.md)
- [App.Server](../objects/App.Server.md)
- [App.Client](../objects/App.Client.Client.md)

```
python tool.py -view App.Client
```
