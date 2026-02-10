App creates the list of the objects at the start. It takes them from current working directory. That's allows to get Object by name and know in advance count of them.

Custom objects can be added with new Namespaces (`objects.index.namespaces`). You can place them at the Custom dir, it ignored in common Namespace.

However, custom objects can load malware, so the Namespace doesn't loads module after finding a file by default, but it still did not helps.

Also you can switch between available namespaces with `objects.index.namespaces.current` settings by passing their names
