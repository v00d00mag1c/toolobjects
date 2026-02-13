from App.Objects.Act import Act
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Responses.ObjectsList import ObjectsList
from App.Objects.Arguments.Assertions.NotNone import NotNone
from App.Objects.Arguments.Argument import Argument
from App.Objects.Arguments.ListArgument import ListArgument
from Data.Types.Int import Int
from Data.Types.String import String
from Data.Types.Boolean import Boolean
from App.DB.Query.Condition import Condition
from App.DB.Query.Values.Value import Value
from App.DB.Query.Sort import Sort
from App.Storage.Item.StorageItem import StorageItem
from App.Storage.StorageUUID import StorageUUID
from App import app

class Search(Act):
    @classmethod
    def _arguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
            ListArgument(
                name = 'storage',
                orig = String,
                #orig = StorageItem,
                #assertions = [NotNone()]
            ),
            Argument(
                name = 'q',
                orig = String,
                default = None
            ),
            Argument(
                name = 'q.in_description',
                orig = Boolean,
                default = False
            ),
            ListArgument(
                name = 'conditions', # Conditions that will be applied before count()
                default = [],
                orig = Condition
            ),
            ListArgument(
                name = 'offset_conditions', # Conditions that will be applied after count(), offset or something
                default = [],
                orig = Condition
            ),
            ListArgument(
                name = 'sort',
                default = [],
                orig = Sort
            ),
            Argument(
                name = 'limit',
                orig = Int,
                default = 30
            ),
            Argument(
                name = 'only_public',
                orig = Boolean,
                default = True
            ),
            Argument(
                name = 'storage_root_if_no_collection',
                orig = Boolean,
                default = True
            ),
            Argument(
                name = 'storage_root_if_no_collection.recursively',
                orig = Boolean,
                default = True
            ),
            Argument(
                name = 'show_tmp',
                orig = Boolean,
                default = False
            ),
            ListArgument(
                name = 'only_object',
                orig = String,
                default = []
            ),
            ListArgument(
                name = 'linked_to',
                default = None,
                orig = StorageUUID
            ),
            Argument(
                name = 'linked_to.recursively',
                default = True,
                orig = Boolean
            ),
            ListArgument(
                name = 'not_linked_to',
                default = None,
                orig = StorageUUID
            ),
            Argument(
                name = 'not_linked_to.recursively',
                default = True,
                orig = Boolean
            ),
            ListArgument(
                name = 'uuids',
                default = None,
                orig = StorageUUID
            ),
        ])

    async def _implementation(self, i) -> ObjectsList:
        _objects = ObjectsList(items = [], unsaveable = True)
        _storage = i.get('storage')
        storages = list()
        if len(_storage) == 0:
            storages = app.Storage.items
        else:
            for _item in i.get('storage'):
                storages.append(app.Storage.get(_item))

        for storage in storages:
            try:
                _query = await self._search_in_storage(i, storage)
                _objects.total_count += _query.count()

                for item in _query.getAll():
                    try:
                        _objects.append(item.toPython())
                    except Exception as e:
                        self.log_error(e, exception_prefix = f"{item.uuid} not printing: ")
            except Exception as e:
                self.log_error(e)

        return _objects

    async def _search_in_storage(self, i, storage):
        _query = storage.adapter.getQuery()
        for condition in i.get('conditions'):
            _query.addCondition(condition)

        in_root = True
        for key in ['linked_to', 'not_linked_to']:
            _operator = {'linked_to': 'in', 'not_linked_to': 'not_in'}[key]
            _ids = list()
            _val = i.get(key)
            if len(_val) == 0:
                continue

            if key == 'linked_to':
                in_root = False

            recursively = i.get(key + '.recursively')

            for link in _val:
                _item = link.getItem()
                if _item == None:
                    self.log(f"{link.getId()}: not exists in this db")
                    continue

                links = None
                if recursively:
                    links = _item.toPython().getLinksRecurisvely()
                else:
                    links = await _item.toPython().asyncGetLinked()

                for linked_item in links:
                    if linked_item.item.hasDb() == False:
                        continue

                    _ids.append(linked_item.item.getDb().uuid)

            _query.addCondition(Condition(
                val1 = Value(
                    column = 'uuid'
                ),
                operator = _operator,
                val2 = Value(
                    value = _ids
                )
            ))

        if in_root and i.get('storage_root_if_no_collection'):
            _2_uuids = list()
            root_collection = storage.get_root_collection()

            if root_collection:
                recursively = i.get('storage_root_if_no_collection.recursively')

                links = None
                if recursively:
                    links =  root_collection.getLinksRecurisvely()
                else:
                    links = await root_collection.asyncGetLinked()

                for link in links:
                    _2_uuids.append(link.item.getDbId())

                _query.addCondition(Condition(
                    val1 = Value(
                        column = 'uuid'
                    ),
                    operator = 'in',
                    val2 = Value(
                        value = _2_uuids
                    )
                ))

        if len(i.get('uuids')) > 0:
            _ids_check = list()
            for item_id in i.get('uuids'):
                _ids_check.append(item_id.uuid)

            _query.addCondition(Condition(
                val1 = Value(
                    column = 'uuid'
                ),
                operator = 'in',
                val2 = Value(
                    value = _ids_check
                )
            ))

        if i.get('only_public'):
            _query.addCondition(Condition(
                val1 = Value(
                    column = 'content',
                    json_fields = ['local_obj', 'public']
                ),
                operator = '==',
                val2 = Value(
                    value = True
                )
            ))

        if i.get('show_tmp') == False:
            _query.addCondition((
            Condition(
                val1 = Value(
                    column = 'content',
                    json_fields = ['obj', 'is_tmp']
                ),
                operator = '==',
                val2 = Value(
                    value = None
                )
            )))

        q = i.get('q')
        if q and len(q) > 0:
            _conditions = list()
            for key in ['local_obj', 'obj']:
                _conditions.append(Condition(
                val1 = Value(
                    column = 'content',
                    json_fields = [key, 'name']
                ),
                operator = 'contains',
                val2 = Value(
                    value = q
                )
            ))

            if i.get('q.in_description'):
                for key in ['local_obj', 'obj']:
                    _conditions.append(Condition(
                        val1 = Value(
                            column = 'content',
                            json_fields = [key, 'description']
                        ),
                        operator = 'contains',
                        val2 = Value(
                            value = q
                        )
                    ))

            # "OR"
            _query.addCondition(_conditions)

        only_objects = i.get('only_object')
        if only_objects and len(only_objects) > 0:
            _query.addCondition(Condition(
                val1 = Value(
                    column = 'content',
                    json_fields = ['obj', 'saved_via', 'object_name']
                ),
                operator = 'in',
                val2 = Value(
                    value = only_objects
                )
            ))

        for condition in i.get('sort'):
            _query.addSort(condition)

        for condition in i.get('offset_conditions'):
            _query.addCondition(condition)

        if i.get('limit') > 0:
            _query.limit(i.get('limit'))

        return _query
