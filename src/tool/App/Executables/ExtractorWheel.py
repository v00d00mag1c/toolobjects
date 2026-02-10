from App.Arguments.Comparer import Comparer
from App.Responses.Response import Response

class ExtractorWheel():
    '''
    Executable that chooses between extractors from submodules.

    По изначальной задумке называлось Representation, и этот класс должен был представлять какой-либо объект, однако позже оно было заменено на Object.
    В общем, не имеет своих экстракторов, является лишь wheel, рычагом между несколькими экстракторами
    '''

    async def implementation(self, i) -> Response:
        '''
        Overrides the default Executable.Execute "implementation()" and allows for automatic extractor choosing
        You should not override this. it's better to create single extractor
        '''

        extractors = []
        modules = self.outer.submodules.getInternal(type_in=["Extractor", "Receivation"])
        for submodule in modules:
            if submodule.submodule_value != 'internal':
                continue

            extractors.append(submodule)

        extractor = self._getSuitableExtractor(extractors, i)
        assert extractor != None, "can't find suitable extractor"

        self.log(f"Using extractor: {extractor.meta.class_name_str}")

        extract = extractor()
        extract.parent = self.outer
        extract.call = self.outer.call

        return await extract.execute.execute(i)

    def _getSuitableExtractor(self, items: list, values: dict):
        for item in items:
            decl = Comparer(compare = item.arguments.recursive_args, values = values)

            if decl.diff():
                return item

        return None

    def _getOptimalStrategy(self):
        pass
