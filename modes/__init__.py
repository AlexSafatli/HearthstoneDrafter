''' Interface and other definitions needed to create game modes for the drafting engine. '''

import os
from abc import ABCMeta as abstractclass, abstractmethod

# Definition of how many cards a set draft should have.
HS_NUM_CARDS_IN_SET = 3

# Private definitions; boilerplate for module definition.
thisdir = os.path.split(os.path.realpath(__file__))[0]
itlist = os.listdir(thisdir)
__all__ = [os.path.split(x)[-1].strip('\.py') for x in itlist if x.endswith('py') and not x.endswith('__init__.py')]

# Class definition for a game mode; interface.
class gameMode(object):
    __metaclass__ = abstractclass
    def __init__(self,coll,hero,info):
        self.name = ''
        self.collection = coll
        self.hero = hero
        self.info = info        
    @abstractmethod
    def getDraft(self,numCards): return []
