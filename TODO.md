core:

- [x] Object
- [x] App
- [x] Objects list
- [x] Views
- [x] Arguments
- [x] ArgumentDict
- [x] hooks need to be refactored (its impossible to debug this)
- [x] switchextractor
- [x] queue
- [ ] queue: repeat (or Queue's settings)
- [ ] App.Queue.ValueWithReplaces
- [x] App.Storage.StorageUnit
- [x] App.Storage.StorageUnitStorage
- [x] App.Objects.Client
- [x] App.Objects.Submodules
- [x] App.Objects.Linkable
- [x] App.Config.Config
- [x] App.Console.PrintLog
- [x] logger: section skips
- [x] logger: output to file
- [x] ~~App.Executables.Call list~~ List of running executables
- [x] flushed object: allow to override name (ObjectMeta.object_names)
- [x] ~~add collections?~~ allow to override getLinks
- [x] Configurable: role of the argument 'env' or 'config'
- [x] daemon, App.Daemons.StartDaemon, implementation_cycle() (?)
- [x] name of object required twice
- [x] namespace: load submodules
- [x] ~~remove Optional required by model_validate~~
- [ ] keep spaces in brackets in _parse_argv, choose another argparser
- [x] App.Objects.Operations.Edit
- [x] App.ReloadModules

db and storage:

- [x] get rid of saveable
- [x] Executable.common_object: move to submodule with common name
- [x] declare requirements that module uses
- [x] db flush: move links
- [x] allow to replace some field with link
- [x] db flush: replaced links
- [x] db flush: when loading from db save the link to db's item and add sync between them
- [x] objects list: split to Namespace, allow to add another object lists
- [x] arguments strangely passes to executable
- [x] extra fields are not saving
- [x] db flush: export between dbs
- [x] argument: default env val
- [x] VirtualPath
- [x] DisplayType (?) submodule=displayment
- [x] App.DB.Search
- [ ] App.Storage.Movement.Export and App.Storage.Movement.Import with zip
- [ ] App.Storage.Movement.ExportAsFiles
- [ ] objectlist adapter
- [x] link after save
- [x] search in linked
- [x] Web.DownloadManager.Manager
- [ ] storageunit generates hash randomly but maybe hash the common file?
- [ ] storageunit flush_hook and getCommonDir(): pathlib parts are duplicated and its better to move to HashDir class
- [ ] links order
- [ ] links are not optimized and paginated
- [ ] multifile config
- [x] link to storageunit file (StorageUnitLink)
- [ ] remove console and to_json differences
- [ ] advanced Conditions (val1 % val2 > 0 or smth)

- [ ] VirtualPath

auth:

- [x] App.ACL.AuthLayer
- [ ] ItemPermission for dbs
- [ ] ~~tokens~~

modules:

- [x] Data.XML
- [x] Files.FileManager.Navigate
- [ ] move File.FileTypes.Image
- [ ] App.Config.Set
- [ ] App.Config.Get
- [ ] App.Logger.List
- [ ] App.Logger.GetFile
- [ ] Web.RSS.GetFeed
- [x] Media.Text.Text
- [x] Abstract.TODO or Abstract.Checkmarks

web:

- [x] WebServer
- [ ] websocket connection: set event_index in executable to distinguish variables messages
- [ ] main blocks
- [ ] displaytype=js_module
- [ ] svelte modules

others:

- [ ] Remove Arguments and Variable functions and move them to submodules system with role=validation or role=variable
- [ ] custom object can contain "source" and "meta" fields in it and replace the original, so name it differently?
- [ ] object that can contain self subtypes, for example File can be imagined as Image with file field. ObjectsList.findByMRO
- [ ] there is similar functions: Configurable.getAllSettings, Validable.getAllArguments, Submodulable.getAllSubmodules, Variableable.getAllVariables, no functions to skip one of mro's item. maybe move it to MROThing
- [ ] env variables and arguments are separate but theyre similar by usage. Argument should contain 'env' field, and if value is not passed, take value from env
- [ ] Namespace: allow to not fallback to common
- [ ] ~~executable with "through" type, or "proxy" idk. for example, act that saves and runs after main~~
- [ ] safety: permissions per every class
- [ ] restrictedpython when importing
- [ ] Example: App.Storage.Movement.Import. mount_name is None by default, and if its not, its sets that the name from last part. and maybe its better to set default as lambda function?
- [ ] App.Storage.Movement.Save and App.Storage.Movement.Export are the same
- [ ] App.Objects.View can be imagined as App.Objects.Displayment
- [ ] App.Object.Paginable
- [ ] storage unit password & encryption)
- [ ] App.Storage.Movement* acts logically should belong to App.DB*
- [ ] link with parent=None to link to the db (there is `root_uuid` anyway, this solution is ненаглядно)
- [ ] LinkInsertion must be changed after flushing from db (but i did workaround with self._get() function)
