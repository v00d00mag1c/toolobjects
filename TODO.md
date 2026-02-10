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
- [x] move App.Data.DictList to App.Objects.DictList
- [x] logger: section skips
- [x] logger: output to file
- [x] ~~App.Executables.Call list~~ List of running executables
- [x] flushed object: allow to override name (ObjectMeta.object_names)
- [x] ~~add collections?~~ allow to override getLinks
- [x] Configurable: role of the argument 'env' or 'config'
- [x] daemon, App.Daemons.StartDaemon, implementation_cycle() (?)

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
- [ ] db flush: export between dbs
- [ ] objectlist adapter
- [ ] argument: default env val
- [x] VirtualPath
- [ ] VirtualPath pagination (adapter pagination also)
- [ ] DisplayType (?) submodule=displayment
- [ ] Web.DownloadManager.Manager
- [ ] storageunit generates hash randomly but maybe hash the common file?
- [ ] storageunit flush_hook and getCommonDir(): pathlib parts are duplicated and its better to move to HashDir class

auth:

- [ ] App.ACL.Auth ?

modules:

- [x] Data.XML
- [x] Files.FileManager.Navigate
- [ ] File.FileTypes.Image
- [ ] App.Config.Set
- [ ] App.Config.Get
- [ ] App.Logger.List
- [ ] App.Logger.GetFile
- [ ] Web.RSS.GetFeed
- [ ] Data.Text
- [ ] Abstract.TODO or Abstract.Checkmarks

documentation:

- [ ] objects
- [ ] objects loading
- [ ] link

web:

- [ ] main blocks
- [ ] displaytype=js_module

others:

- [ ] Remove Arguments and Variable functions and move them to submodules system with role=validation or role=variable
- [ ] custom object can contain "source" and "meta" fields in it and replace the original, so name it differently?
- [ ] object that can contain self subtypes, for example File can be imagined as Image with file field. ObjectsList.findByMRO
- [ ] there is similar functions: Configurable.getAllSettings, Validable.getAllArguments, Submodulable.getAllSubmodules, Variableable.getAllVariables, no functions to skip one of mro's item. maybe move it to MROThing
- [ ] env variables and arguments are separate but theyre similar by usage. Argument should contain 'env' field, and if value is not passed, take value from env
- [ ] Namespace: allow to not fallback to common
- [ ] executable with "through" type, or "proxy" idk. for example, act that saves and runs after main
