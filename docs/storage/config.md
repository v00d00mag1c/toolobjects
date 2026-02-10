Object needs a place to store settings. So there is Configurable that allows to define settings of every class and Config. At the and of the objects list generation, it will add every object options to Config compare values. Input values will be taken from the config.json file.

Env is also a config but for sensitive data, values also are taking from json file.

You should name options like:

`{class or topic name}.{part of the class or functionality}.{name of the option}`
