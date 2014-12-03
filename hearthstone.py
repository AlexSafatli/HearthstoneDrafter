from random import choice, uniform
import json

HS_CARD_DATA   = 'data/cards.json'
HS_RARITY_RANK = {0:'Free',1:'Common',2:'Rare',3:'Epic',4:'Legendary'}

class drafter(object):

    def __init__(self,preferred_hero=None):

      self.hero       = preferred_hero
      self.collection = HearthstoneCollection()
      self.sets       = []      
    
    def _makeSequenceOfApplicableCards(self,rarity):

        coll = self.collection
        itercards = lambda d: coll.iterCardsForRarity(HS_RARITY_RANK[d])

        # Get all cards.
        cards = [card for card in itercards(rarity) if not card.getHero() or card.getHero() == self.hero.getHero()]

        # Couple basic and common cards.                                                                 
        if rarity == 1:
            cards += [card for card in itercards(0) if not card.getHero() or card.getHero() == self.hero.getHero()]

        # Go through and only return cards that are class types.
        return cards

    def _getSet(self,curr=1):

        # See what tier of rarity.
        currRarity = curr
        random     = uniform(0,1)
        while random <= 0.2 and currRarity < len(HS_RARITY_RANK) - 1:
            # Upgrade to the next tier!
            currRarity += 1
            random = uniform(0,1)
        
        # Assign a set of three cards of this rarity type.
        cards = self._makeSequenceOfApplicableCards(currRarity)
        set   = []
        for x in xrange(3):
            card = choice(cards)
            while card in set:
                card = choice(cards)
            set.append(card)
        return tuple(set)

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
        return sorted(cards,key=lambda d: d.getCost())
        
    def get(self):
    
        ''' Make the draft of thirty sets of three cards. '''

        # Random hero.
        if self.hero is None or self.hero not in self.collection.getHeroNames():
            self.hero = choice(self.collection.getHeroes())
        elif self.hero in self.collection.getHeroNames():
            self.hero = self.collection.getHeroes()[self.collection.getHeroNames(
                    ).index(self.hero)]
      
        # Random cards.
        for set in xrange(30):
            if set in [0,9,19,29]:
                self.sets.append(self._getSet(2))
            else: self.sets.append(self._getSet())

        return (self.hero,self.sets)

class HearthstoneDataFile(object):
    
    def __init__(self,pathToFile):
        
        self.path  = pathToFile
        self.handl = open(self.path)
        self.data  = json.load(self.handl)
        self.types = self.data.keys()
        self.rarities = []
        self.handl.close()

    def iterCards(self):

        for typekey in self.types:
            for carddata in self.data[typekey]:
                cardid   = carddata['id']
                cardname = carddata['name']
                if 'cost' in carddata: cardcost = carddata['cost']
                else: cardcost = 0
                if 'collectible' in carddata:
                    cardcoll = carddata['collectible']
                else: cardcoll = False
                if 'playerClass' in carddata:
                    cardhero = carddata['playerClass']
                else: cardhero = None
                if 'rarity' in carddata:
                    cardrarity = carddata['rarity']
                    if cardrarity not in self.rarities: self.rarities.append(cardrarity)
                else: cardrarity = 'None'
                cardtype = typekey
                yield self._makeCard(cardid,cardname,cardcost,cardcoll,cardrarity,cardhero,cardtype)

    def _makeCard(self,id,name,cost,coll,rarity,hero,type):
        return HearthstoneCard(id,name,cost,coll,rarity,hero,type)

class HearthstoneCollection(object):

    def __init__(self):

        self.datafile = HearthstoneDataFile(HS_CARD_DATA)
        self.heroes   = []
        self.types    = []
        self.cards    = self._readCardData()

    def _readCardData(self):

        carddata = {}

        for card in self.datafile.iterCards():
            if card.getID().startswith('HERO'):
                self.heroes.append(card)
            elif not card.getID()[-1].isalpha() and not card.getName() == 'AFK' and card.isCollectible():
                if card.getType() not in carddata:
                    carddata[card.getType()] = []
                    self.types.append(card.getType())
                carddata[card.getType()].append(card)
                
        return carddata
                    
    def getRarities(self): return self.datafile.rarities
    def getTypes(self): return self.types
    def iterCardsForType(self,ty): return [card for card in self.cards[ty]]

    def iterCardsForRarity(self,rar):
        for type in self.getTypes():
            for card in self.iterCardsForType(type):
                if card.getRarity() == rar: yield card
 
    def getHeroes(self):    return self.heroes
    def getHeroNames(self): return [x.getHero() for x in self.heroes]
 

class HearthstoneCard(object):
    
    def __init__(self,id='',name='',cost=0,collectible=True,rarity='Free',hero=None,type=''):
        
        self.id = id
        self.name = name
        self.cost = cost
        self.collectible = collectible
        self.rarity = rarity
        self.hero = hero
        self.type = type

    def getID(self): return self.id
    def getName(self): return self.name
    def getCost(self): return self.cost
    def isCollectible(self): return self.collectible
    def getRarity(self): return self.rarity
    def getType(self): return self.type
    def getHero(self): return self.hero
	
    def getImgLink(self):

        return 'http://wow.zamimg.com/images/hearthstone/cards/enus/original/%s.png' % (self.id)

    def getPlainStr(self):

        return '%s (%d)' % (self.name,self.cost)
    
    def toDebugString(self):

        return '[%s:%s:%s] (%d) <For Hero: %s> <Type: %s>' % (self.name,self.rarity,self.id,self.cost,self.hero,self.type)

    def __str__(self):
        
        str = '<span class="rarity_%s">%s</span>' % (self.rarity,self.name)
        if self.getHero() is not None: str = '<span class="card_Spell">' + str + '</span>'
        return str + ' (%d)' % (self.cost)
