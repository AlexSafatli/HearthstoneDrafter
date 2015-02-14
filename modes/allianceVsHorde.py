''' Alliance vs. Horde Game Mode, based on an idea that a friend of mine suggested to me once. Draft cards randomly from the entire set with the only restriction being that they are (1) a class card or (2) not a class card BUT of a certain faction (Horde/Alliance). Definitions of card factions have been customly patched as defined in the factions.json file (see root directory of repository). '''

from __init__ import gameMode as mode, HS_NUM_CARDS_IN_SET
from random import uniform, choice
import copy

name = 'Alliance vs. Horde'
key  = 'allianceVsHorde'
options = ['Alliance','Horde']
description = "Battle a friend as one of the <strong>factions</strong> of Azeroth! Pandarens, dragons, and other related creatures are <em>neutral</em>."

class gameMode(mode):
    
    def __init__(self,coll,hero,info):
        super(gameMode,self).__init__(coll,hero,info)
        self.cards = list()
    
    def tooManyCards(self,card): # Quick hack; make sure the draft only has enough cards in it that you can put into a normal hearthstone deck.
        if card.getRarity() == 'Legendary': return (card in self.cards)
        else: return (self.cards.count(card) == 2)
    
    def getSet(self):
        coll = self.collection
        hero = self.hero
        cards = [card for card in coll.iterCards() if self.isApplicableCard(card)]
        set   = list()
        for x in xrange(HS_NUM_CARDS_IN_SET):
            card = choice(cards)
            while (card in set or self.tooManyCards(card)):
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
