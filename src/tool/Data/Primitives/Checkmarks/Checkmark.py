from App.Objects.Object import Object
from App.Objects.Act import Act
from App.Objects.Relations.LinkInsertion import LinkInsertion
from App.Objects.Operations.Create.CreationItem import CreationItem
from pydantic import Field

class Checkmark(Object):
    state: bool = Field(default = False)
    label: str | LinkInsertion = Field(default = None)

    def get_label_text(self):
        label = self._get('label')
        if label == None:
            return '...'

        if type(label) == str:
            return label
        else:
            return 'label no text'

    def _display_as_string(self):
        _mark = "[ ]"
        if self.state:
            _mark = "[x]"

        _label = self._get('label')
        _label_text = ""

        if _label != None:
            _label_text = _label.value

        return "\n" + _mark + " " + _label_text + ' \n'

    @classmethod
    def _creations(cls) -> list:
        return [
            CreationItem(
                name = 'TODO List',
                object_name = 'Data.Primitives.Checkmarks.List',
                create = 'Data.Primitives.Checkmarks.CreateList'
            ),
        ]
