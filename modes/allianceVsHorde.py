# Arena Game Mode

from __init__ import gameMode as mode
from random import uniform, choice
import copy

name = 'Alliance vs. Horde'
key  = 'allianceVsHorde'
options = ['Alliance','Horde']
description = "Battle a friend as one of the <strong>factions</strong> of Azeroth!"

class gameMode(mode):
    
    def __init__(self,coll,hero,info):
        super(gameMode,self).__init__(coll,hero,info)
        self.cards = []
    
    def tooManyCards(self,card):
        if card.getRarity() == 'Legendary': return (card in self.cards)
        else: return (self.cards.count(card) == 2)
    
    def getSet(self):
        
        coll = self.collection
        hero = self.hero
        itercards = lambda: coll.iterCards()
        
        cards = [card for card in itercards() if self.isApplicableCard(card)]
        set   = []
        for x in xrange(3):
            card = choice(cards)
            while (card in set) or (self.tooManyCards(card)):
                card = choice(cards)
            self.cards.append(card)
            set.append(copy.deepcopy(card))
        return tuple(set)
        
    def isApplicableCard(self,card):
        
        return (card.getHero() and card.getHero() == self.hero.getHero()
                ) or (not card.getHero() and card.getFaction() == self.info['faction'])
    
    def getDraft(self,numCards):
        
        sets = []
        for set in xrange(numCards): sets.append(self.getSet())
        return sets