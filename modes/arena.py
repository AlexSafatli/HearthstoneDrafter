# Arena Game Mode

from __init__ import gameMode as mode
from random import uniform, choice
from copy import deepcopy as new

HS_RARITY_RANK    = {0:'Free',1:'Common',2:'Rare',3:'Epic',4:'Legendary'}
HS_UPGRADE_CHANCE = 0.2

name = 'Arena'
key  = 'arena'
description = "Emulate the standard Hearthstone arena and practice drafting by creating a mock deck."

class gameMode(mode):
    
    def getCardsForRarity(self,rarity):
        
        coll   = self.collection
        icards = lambda d: coll.iterCardsForRarity(HS_RARITY_RANK[d])
    
        # Get all cards.
        cards = [card for card in icards(rarity) if 
                 self.isApplicableCard(card)]
    
        # Couple basic and common cards.                                                                 
        if rarity == 1:
            cards += [card for card in icards(0) if 
                      self.isApplicableCard(card)]
    
        # Go through and only return cards that are class types.
        return cards   
    
    def isApplicableCard(self,card): 
      
        return (not card.getHero() or card.getHero() == self.hero.getHero())    
    
    def getSet(self,currRarity=1):
        
        # See what tier of rarity.
        random = uniform(0,1)
        while random <= HS_UPGRADE_CHANCE and currRarity < len(HS_RARITY_RANK) - 1:
            # Upgrade to the next tier!
            currRarity += 1
            random = uniform(0,1)
        
        # Assign set of 3 cards of this rarity.
        cards = self.getCardsForRarity(currRarity)
        set   = []
        for x in xrange(3):
            card = choice(cards)
            while card in set:
                card = choice(cards)
            set.append(new(card))
        return tuple(set)     
    
    def getDraft(self,numCards):
        
        ''' Make a draft of numCards sets of three cards. '''
        
        sets = []
        for set in xrange(numCards):
            if set in [0,9,19,29]:
                sets.append(self.getSet(2))
            else: sets.append(self.getSet())
        return sets
            
        
