from App.Objects.Object import Object
from App.Objects.Act import Act
from App.Objects.Relations.LinkInsertion import LinkInsertion
from Data.Types.String import String
from pydantic import Field

class Checkmark(Object):
    state: bool = Field(default = False)
    label: String | LinkInsertion = Field(default = None)

    def _display_as_string(self):
        _mark = "[ ]"
        if self.state:
            _mark = "[x]"

        _label = self._get('label')
        _label_text = ""

        if _label != None:
            _label_text = _label.value

        return "\n" + _mark + " " + _label_text + ' \n'
