from App.Objects.Object import Object
from pydantic import Field
from App.Logger.Log import Log
from typing import Literal

class HideCategory(Object):
    '''
    Object of logger.hide_sections param that allows to hide some messages from logging

    section: section that not will be showed
    wildcard: will check first items of section, if section of log contains them so its true

    section=["App", "Index"] wildcard=False input_section=["App", "Index", "LoadedObject"] === no
    section=["App", "Index"] wildcard=True input_section=["App", "Index", "LoadedObject"] === yes

    unused: do not count this hidecategory

    where: may be console, web, file or smth
    '''

    section: list = Field(default = None)
    role: str = Field(default = None)
    where: list[Literal['console', 'file']] = Field(default = None)
    wildcard: bool = Field(default = False)
    unused: bool = Field(default = False)

    def isLogMeets(self, log: Log, context: str = None) -> bool:
        '''
        Defines does log needs to be hidden (true or false)
        '''

        if self.unused == True:
            return False

        try:
            assert self.isSectionMeets(log.section.value)
            assert self.isRoleMeets(log.role)
            assert self.isContextMeets(context)
        except:
            return False

        return True

    def isSectionMeets(self, section: list[str]) -> bool:
        if self.section == None:
            return True

        if self.wildcard == True:
            if len(section) == 0:
                return True

            return ".".join(section).startswith(".".join(self.section))
        else:
            return ".".join(section) == ".".join(self.section)

    def isRoleMeets(self, role: list[str]) -> bool:
        if self.role != None:
            return self.role in role

        return True

    def isContextMeets(self, context: str) -> bool:
        if self.where != None:
            return context in self.where

        return True
