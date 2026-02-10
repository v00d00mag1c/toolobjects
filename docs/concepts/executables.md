When you described an object, you need a thing that will create them for you, or any thing that will do some action. So there is the Executable object: it contains execution and validation interface. It uses a command pattern. It has subtypes:

**Act**: does action that can has any response

**Extractor**: returns only Object items

**Test**: Act with test purpose

**Convertation**: convert one type of object to another

**View**: representation of the App on platform (eg. Console)

**Wheel**: choose between submodules

**Client**: wheel with client functions
