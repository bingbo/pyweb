from RenderA import *
from RenderB import *


class RenderImpl:
    __renderMap = {};

    def __init__(self):
        self.__renderMap[1] = RenderA()
        self.__renderMap[2] = RenderB()

    def render(self,type):
        self.__renderMap[type].render()
