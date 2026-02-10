from App.Objects.Object import Object
from App import app
from pydantic import Field
from typing import Literal, List
from App.Arguments.ArgumentsDict import ArgumentsDict

class Item(Object):
    '''
    Item of Queue.

    predicate: object that will be called
    constructor_arguments: dict with App.Queue.Argument values that will be used for constructor()
    arguments: dict with App.Queue.Argument values that calls execute()

    if you calling just an Object only constructor_arguments will be used
    '''
    predicate: str = Field()
    build: dict = Field(default = {})
    arguments: dict = Field(default = {})
