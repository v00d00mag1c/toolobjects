There is authentification system. 

### List of users

`app.auth.users` in config allows you to pass all the users:

```
    "app.auth.users": [
        {
            "name": "test",
            "password_hash": "123"
        }
    ]
```

if `root` not in this list, it will be created anyway with password `root`. Root password can be changed by passing him in config

to generate `password_hash`, call `App.ACL.GetHash`:

```
> python tool.py -i App.ACL.GetHash -string 123
```

### Logging in

`App.ACL.AuthLayer` provides `login` function. In `Console` view, you can pass `-username` and `-password` to log as someone

There is tokens that are not implemented yet

### Permissions

**App.ACL.Permissions.ObjectPermission**

Permission to use object by some user. By default, non-root user can't use any object. The name of object passed in `object_name`, the name of user in `user`. Example:

```
    "app.auth.permissions": [
        {
            "object_name": "App.Data.Text",
            "user": "test",
            "allow": true
        }
    ]
```

By default, permissions are checked only in common executor, but with `app.auth.every_call_permission_check` check will happen every execute() call

**App.ACL.Permissions.ItemPermission**

Permission for DB item (that is already flushed)

#### Setting permissions

As shown above, you can pass them in config file. Also you can use `App.ACL.Permissions.SetPermission`
