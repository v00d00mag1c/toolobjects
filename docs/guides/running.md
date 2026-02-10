### Running app

`PowerShell`:

```
> cd {dir}/src
> .\venv.ps1
> .\update.ps1
> .\cd_tool.ps1
> python tool.py -i App.Objects.Requirements.InstallEvery
```

Firstly we cd into `src` folder, entering python virtual environment and installing dependencies. Then we cd into `tool` folder. Optionally, we can install every

I may recomend set these values in `storage/config/config.json`:

```
    "logger.print.exclude": [
        {
            "role": "objects_loading"  
        },
        {
            "role": "empty_response"  
        },
        {
            "section": ["App.Console.ConsoleView"]
        },
        {
            "role": "auth_from_console"
        },
        {
            "section": ["App.Objects.Operations.DefaultExecutorWheel"]
        }
    ],
    "logger.print.db": false,
    "logger.print.console.show_time": false,
    "logger.print.console.show_role": true
```
