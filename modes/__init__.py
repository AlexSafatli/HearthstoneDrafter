import os
from abc import ABCMeta as abstractclass, abstractmethod
thisdir = os.path.split(os.path.realpath(__file__))[0]
itlist = os.listdir(thisdir)
__all__ = [os.path.split(x)[-1].strip('.py') for x in itlist if x.endswith('.py') and not x.endswith('__init__.py')]

class gameMode(object):
    
    __metaclass__ = abstractclass
    
    def __init__(self,coll,hero,info):
        self.name = ''
        self.collection = coll
        self.hero = hero
        self.info = info
        
    @abstractmethod
    def getDraft(self,numCards): return []