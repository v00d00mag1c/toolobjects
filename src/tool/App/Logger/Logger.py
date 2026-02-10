from App.Objects.Object import Object
from App.Console.PrintLog import PrintLog
from App.Logger.HideCategory import HideCategory
from App.Objects.Arguments.Argument import Argument
from App.Objects.Arguments.ListArgument import ListArgument
from Data.Boolean import Boolean
from .Log import Log
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
    def getClassEventTypes(cls) -> list:
        return ['log']

    @classmethod
    def mount(cls):
        from App import app

        logs_dir = app.app.storage.joinpath("logs")
        logs_dir.mkdir(exist_ok = True)

        logger = cls(
            hidden_categories = app.Config.get("logger.print.exclude"),
        )
        logger.log_to_console = logger.getOption('logger.print.console')

        if app.Config.get("logger.print.file") == True:
            logger.log_file = LogFile.autoName(logs_dir)
            logger.log_file.open()

        app.mount('Logger', logger)

    def log(self, 
            message: str | Exception, 
            section: str | list = ['Nonce'],
            role: list[str] = [],
            prefix: LogPrefix = None, 
            exception_prefix: str = '',
            trigger: bool = True):

        write_message = message
        if isinstance(message, Exception):
            exc = traceback.format_exc()
            write_message = exception_prefix + type(message).__name__ + " " + exc

        msg = Log(
            message = write_message,
            role=role
        )
        msg.section = LogSection(value = section)
        if prefix != None:
            msg.prefix = prefix

        if trigger == True:
            self.triggerHooks('log', 
                to_print = msg, 
                check_categories = self.hidden_categories,
            )

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
        return [
            ListArgument(
                name = 'logger.print.exclude',
                default = [],
                orig = HideCategory
            ),
            Argument(
                name = 'logger.print.file',
                default = False,
                orig = Boolean
            ),
            Argument(
                name = 'logger.print.console',
                default = True,
                orig = Boolean
            ),
            Argument(
                name = 'logger.print.console.show_role',
                default = False,
                orig = Boolean
            ),
            Argument(
                name = 'logger.print.console.show_time',
                default = True,
                orig = Boolean
            )
        ]
