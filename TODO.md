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
- [x] queue: repeat (or Queue's settings)
- [x] App.Objects.Queue.ValueWithReplaces
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
- [ ] keep spaces in brackets in `_parse_argv`, choose argparser that supports it
- [x] App.Objects.Operations.Edit
- [x] App.ReloadModules
- [x] advanced arguments
- [ ] fix submodules dups

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
- [x] ~~DisplayType (?) submodule=displayment~~
- [x] App.DB.Search
- [x] App.Storage.Movement.Export and App.Storage.Movement.Import with zip
- [x] App.Storage.Movement.ExportAsFiles
- [x] objectlist adapter
- [x] link after save
- [x] search in linked
- [x] Web.DownloadManager.Manager
- [x] storageunit flush_hook and getCommonDir(): pathlib parts are duplicated and its better to move to HashDir class (StorageAdapter)
- [x] links order
- [ ] links are not optimized and paginated
- [ ] multifile config
- [x] link to storageunit file (StorageUnitLink)
- [x] advanced Conditions (val1 % val2 > 0 or smth)
- [x] storage item.commit()
- [x] remove displayments
- [x] root_uuid
- [ ] App.Storage.CreateRoot
- [x] VirtualPath
- [x] allow to cancel scripts and run them at once

other with objects:

- [x] module downloading
- [x] autostart items
- [ ] allowed_objects that allowed to link to item
- [ ] documentation of the fields

auth:

- [x] App.ACL.AuthLayer
- [x] ItemPermission for dbs
- [ ] permissions for uuids
- [x] tokens

modules:

- [x] Data.XML
- [x] Media.Files.FileManager.Navigate
- [x] move File.FileTypes.Image
- [ ] App.Config.Set
- [x] App.Config.Get
- [ ] ~~App.Logger.List~~
- [ ] ~~App.Logger.GetFile~~
- [x] Web.RSS.GetFeed
- [x] Web.RSS Atom support
- [x] Media.Text.Text
- [x] Abstract.TODO or Abstract.Checkmarks

web crawler:

- [ ] images downloading
- [ ] css assets downloading
- [ ] css assets downloading: data:base64
- [ ] removing scripts mode
- [ ] screenshot taker
- [ ] href and src replacer
- [ ] setting every style of element mode
- [ ] fonts downloading

web:

- [x] WebServer
- [ ] websocket connection: set event_index in executable to distinguish variables messages or smth
- [ ] hook functions for thread and variables
- [ ] displaytype=js_module
- [x] file uploading
- [x] file uploading auth

others:

- [ ] ~~Remove Arguments and Variable functions and move them to submodules system with role=validation or role=variable~~
- [x] ~~custom object can contain "source" and "meta" fields in it and replace the original, so name it differently?~~
- [ ] object that can contain self subtypes, for example File can be imagined as Image with file field. ObjectsList.findByMRO
- [ ] there is similar functions: Configurable.getAllSettings, Validable.getAllArguments, Submodulable.getAllSubmodules, Variableable.getAllVariables, no functions to skip one of mro's item. maybe move it to MROThing
- [ ] env variables and arguments are separate but theyre similar by usage. Argument should contain 'env' field, and if value is not passed, take value from env
- [ ] Namespace: allow to not fallback to common
- [ ] ~~executable with "through" type, or "proxy" idk. for example, act that saves and runs after main~~
- [ ] safety: permissions per every class
- [ ] restrictedpython when importing
- [ ] Example: App.Storage.Movement.Import. mount_name is None by default, and if its not, its sets that the name from last part. and maybe its better to set default as lambda function?
- [ ] ~~App.Object.Paginable~~
- [ ] storage unit password encryption
- [x] App.Storage.Movement* acts logically should belong to App.DB*
- [ ] ~~LinkInsertion must be changed after flushing from db~~ (self._get() is compromis)
- [ ] ~~remove console and to_json differences~~
- [ ] storageunit generates hash randomly but maybe hash the common file? (no it is imposible because the common file is not known beforehand)
- [ ] db operators as objects implementation (for example addCondition(val1 = 'uuid', operator = '==', val2 = String(max_length = 10, min_length = 2)))
