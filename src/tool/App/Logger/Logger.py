from App.Objects.Object import Object
from App.Console.PrintLog import PrintLog
from App.Logger.HideCategory import HideCategory
from .Log import Log
from .LogKind import LogKind, LogKindEnum
from .LogFile import LogFile
from .LogSection import LogSection
from .LogPrefix import LogPrefix
import traceback
from pydantic import Field

class Logger(Object):
    '''
    Class that prints messages (Log's) into hooked functions
    '''

    log_to_console: bool = Field(default = True)
    hidden_categories: list[HideCategory] = Field(default = [])
    log_file: LogFile = Field(default = None)

    @classmethod
    def getClassEventsTypes(cls) -> list:
        return ['log']

    @classmethod
    def mount(cls):
        from App import app

        logs_dir = app.app.storage.joinpath("logs")
        logs_dir.mkdir(exist_ok = True)

        logger = cls(
            hidden_categories = app.Config.get("logger.hide_sections"),
        )
        logger.log_to_console = logger.getOption('logger.out_to_console')

        if app.Config.get("logger.out_to_file") == True:
            logger.log_file = LogFile.autoName(logs_dir)
            logger.log_file.open()

        app.mount('Logger', logger)

    def log(self, 
            message: str | Exception, 
            section: str | list = ['Nonce'],
            types: list[str] = [],
            kind: str = LogKindEnum.message.value,
            prefix: dict[str, int] = None, 
            exception_prefix: str = '',
            trigger: bool = True):

        write_message = message
        if isinstance(message, Exception):
            exc = traceback.format_exc()
            write_message = exception_prefix + type(message).__name__ + " " + exc

        msg = Log(
            message = write_message,
        )
        msg.section = LogSection(value = section)
        msg.kind =  LogKind(value = kind)
        if prefix != None:
            msg.prefix = LogPrefix(**prefix)

        if trigger == True:
            self.triggerHooks('log', to_print = msg, check_categories = self.hidden_categories)

        return msg

    @staticmethod
    def _shouldPrint(to_print: Log, categories: list, where_name: str):
        for category in categories:
            if category.isLogMeets(to_print, where_name) == True:
                return False

        return True

    def constructor(self):
        def print_log(to_print, check_categories):
            if self.log_to_console == False:
                return

            if self._shouldPrint(to_print, check_categories, 'console') == True:
                items = PrintLog()
                items.implementation({'log': to_print})

        self.addHook('log', print_log)

        async def print_file(to_print, check_categories):
            if self.log_file == None:
                return

            if self._shouldPrint(to_print, check_categories, 'file') == True:
                self.log_file.log(to_print)

        self.addHook('log', print_file)

    @classmethod
    def getSettings(cls):
        from App.Arguments.Objects.List import List
        from App.Arguments.Types.Boolean import Boolean
        from App.Arguments.Objects.Orig import Orig

        '''
        to shut up all messages:

        "logger.hide_sections": [
            {
                "section": [],
                "wildcard": true,
                "kind": ["message"],
                "where": ["console"]
            }
        ],
        '''

        return [
            List(
                name = 'logger.hide_sections',
                default = [],
                orig = Orig(
                    name = 'logger.hide_section',
                    orig = HideCategory
                )
            ),
            Boolean(
                name = 'logger.print_to_file',
                default = False
            ),
            Boolean(
                name = 'logger.print_to_console',
                default = True
            )
        ]
