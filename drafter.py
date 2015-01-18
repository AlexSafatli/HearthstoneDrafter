from hearthstone import HearthstoneCollection
from gameMode import getMode
from random import choice

class drafter(object):

    def __init__(self,preferred_hero=None,mode='arena',tag=None):

        self.hero       = preferred_hero
        self.gamemode   = getMode(mode)
        self.tag        = tag
        self.collection = HearthstoneCollection()
        self.sets       = []
        if self.gamemode == None:
            raise NotImplemented('Game mode %s not defined.' % (mode))

    def __len__(self): return len(self.sets)
    def size(self):    return self.__len__()

    def getNumLegendaries(self):

        return self.getNumOfCardsForRarity('Legendary')

    def getNumOfCardsForRarity(self,rarity):

        ''' Acquire the number of cards in the draft by their rarity (string). '''

        num = 0
        for set in self.sets:
            if set[0].getRarity() == rarity:
                num +=1
        return num

    def getSets(self): return self.sets
    def index(self,i): return self.sets.index(i)

    def getSortedCards(self):

        ''' Return a sorted list of all present cards in the draft. '''

        cards = []
        for set in self.sets:
            for card in set: cards.append(card)
        return sorted(cards,key=lambda d: (d.getCost(),d.getName()))

    def get(self):

        ''' Make the draft of thirty sets of three cards. '''

        # Random hero.
        if self.hero is None or self.hero not in self.collection.getHeroNames():
            self.hero = choice(self.collection.getHeroes())
        elif self.hero in self.collection.getHeroNames():
            self.hero = self.collection.getHeroes()[self.collection.getHeroNames(
                ).index(self.hero)]

        # Random cards.
        self.gamemode = self.gamemode(self.collection,self.hero,self.tag)
        self.sets = self.gamemode.getDraft(30)
        
        # See if gold cards are being requested.
        if 'gold' in self.tag and self.tag['gold']:
            for set in self.sets:
                for card in set:
                    card.setGoldCard(True)

        return (self.hero,self.sets)
