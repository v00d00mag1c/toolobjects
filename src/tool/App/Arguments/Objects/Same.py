from ..Argument import Argument

class Same(Argument):
    '''
    Return the same object that was passed
    '''
    def implementation(self, original_value):
        return original_value
