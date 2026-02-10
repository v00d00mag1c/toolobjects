from App.Objects.Object import Object

class Queue(Object):
    '''
    Class that allows to run multiple executables with his context

    Uses App.Queue.Item for "prestart" and "items".

    prestart - Items that will be executed before the "items". You can pass variables there. Things that does not has "execute()"
    items - Items that will be executed as main process
    output - Queue output format

    The results will be stored at the variables "prestart" and "items".
    You can reference results by "$" for prestart and "#" for items
    '''
    prestart: list = []
    items: list = []
    output: list = []

    def convertArguments(self):
        pass

    def getOutput(self):
        pass
