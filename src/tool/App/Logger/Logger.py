from App.Objects.Object import Object
from App.Console.PrintLog import PrintLog
from .Log import Log
from .LogKind import LogKind, LogKindEnum
from .LogSection import LogSection
from .LogPrefix import LogPrefix
import traceback

class Logger(Object):
    '''
    Class that prints messages (Log's) into hooked functions
    '''

    @classmethod
    def getClassEventsTypes(cls) -> list:
        return ['log']

    @classmethod
    def mount(cls):
        from App import app

        #app.Config.updateCompare()
        logger = cls(
            #skip_file = app.Config.get("logger.output.to_file"),
            #limiter = LogLimiter(skip_categories = app.Config.get("logger.output.filters")),
        )

        app.mount('Logger', logger)

    def constructor(self):
        if True:
            async def print_log(to_print):
                items = PrintLog()
                await items.implementation({'log': to_print})

            self.addHook('log', print_log)

    def log(self, 
            message: str | Exception, 
            section: str | list = ['Nonce'],
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
            self.triggerHooks('log', to_print = msg)

        return msg
