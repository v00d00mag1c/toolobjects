from App.Objects.Act import Act
from App.Objects.Object import Object
from App.Objects.Arguments.ArgumentDict import ArgumentDict
from App.Objects.Arguments.Argument import Argument
from App.Objects.Arguments.ListArgument import ListArgument
from App.Objects.Arguments.Assertions.NotNone import NotNone
from App.Objects.Arguments.Assertions.InputNotInValues import InputNotInValues
from App.Objects.Arguments.ArgumentValues import ArgumentValues
from App.Objects.Responses.ObjectsList import ObjectsList
from App.Storage.Movement.Save import Save
from App.Storage.StorageUUID import StorageUUID
from App.Locale.Documentation import Documentation
from App.Locale.Key import Key
from Data.Types.String import String
from Data.Types.Boolean import Boolean
from pydantic import Field
from typing import Coroutine
from App import app

class DefaultExecutorWheel(Act):
    ev_hooks: list = Field(default = [])

    async def _implementation(self, i: ArgumentValues):
        force_flush = i.get('force_flush')
        item_class = i.get('i')

        assert item_class != None, 'not found object'
        assert app.app.view.canUseObject(item_class), 'object cannot be used at this view'
        assert item_class.canBeUsedBy(i.get('auth')), 'access denied to executable {0}'.format(item_class._getClassNameJoined())

        item_that_executed = None
        results = None
        if force_flush == False:
            assert item_class.canBeExecuted(), 'object does not contains execution interface'

            if callable(item_class):
                item_class = item_class()

            item_class.integrate(i.values)

            # Hooks from websockets workaround

            if hasattr(item_class, 'getVariables') and 'var_update' in item_class.getClassEventTypes():
                for hook in self.ev_hooks:
                    item_class.addHook('var_update', hook)

            results = await item_class.execute(i = i)
        else:
            _vals = i.getValues(exclude = app.app.view.getCompareKeys() + self.getCompareKeys() + ['auth'])

            results = ObjectsList(items = [], unsaveable = False)

            # isinstance(executable, Executable wont work with cls (
            if hasattr(item_class, 'integrate') and i.get('force_flush.as_args'):
                if callable(item_class):
                    item_that_executed = item_class(args = _vals)
                else:
                    item_that_executed = item_class
                    item_that_executed.args = _vals
            else:
                _keys = dict()
                # outside arguments can get there, so saving only values from fields
                for key in item_class._getFieldsNames():
                    if _vals.get(key) == None:
                        continue

                    _keys[key] = _vals.get(key)

                if callable(item_class):
                    item_that_executed = item_class(**_keys)
                else:
                    item_that_executed = item_class

            item_that_executed.obj.is_forced = True
            results.append(item_that_executed)

        if results.isInstance(ObjectsList):
            if results.should_be_saved() == True and i.get('do_save'):
                save_to = i.get('save_to')
                if save_to != None and len(save_to) > 0:
                    try:
                        _new = i.toDict()
                        _new.update({
                            'items': results,
                            'storage': save_to,
                            'auth': i.get('auth'),
                            'ignore_errors': i.get('ignore_errors'),
                            'ignore_flush_hooks': i.get('ignore_flush_hooks', results.ignore_flush_hooks)
                        })

                        await Save().execute(_new)
                    except Exception as e:
                        self.log_error(e)
            else:
                self.log('result cannot be saved')

        return results

    def add_variables_hook(self, hook: Coroutine):
        self.ev_hooks.append(hook)

    @classmethod
    def _arguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
            Argument(
                name = 'i',
                # default = 'App.Objects.Queue.Run',
                orig = Object,
                assertions = [
                    NotNone(),
                    InputNotInValues(values=['App.Console.Console', 'App.Console.Console.Console'])
                ],
                documentation = Documentation(
                    name = Key(
                        value = 'Main object'
                    )
                ),
            ),
            Argument(
                name = 'do_save',
                default = True,
                orig = Boolean
            ),
            ListArgument(
                name = 'save_to',
                default = ['tmp'],
                single_recommended = True,
                documentation = Documentation(
                    name = Key(
                        value = 'Save to storages'
                    ),
                    description = Key(
                        value = 'Names of storages where object will be saved (if it returns ObjectsList)'
                    )
                ),
                orig = String
            ),
            Argument(
                name = 'force_flush',
                orig = Boolean,
                documentation = Documentation(
                    name = Key(
                        value = 'Flush literally'
                    ),
                    description = Key(
                        value = 'Flush to DB (save_to) ignoring execution interface'
                    )
                ),
                default = False
            ),
            Argument(
                name = 'force_flush.as_args',
                orig = Boolean,
                default = True,
                documentation = Documentation(
                    name = Key(
                        value = 'Use as args'
                    ),
                    description = Key(
                        value = 'Use another passed arguments for args field, if force_flush = true and i is an executable'
                    )
                ),
            )
        ],
        missing_args_inclusion = True).join_class(Save, ['link_to', 'link_max_depth', 'public'])
