import json, copy, os

HS_CARD_DATA  = os.path.join(os.path.split(__file__)[0],'cards.json')
HS_FACT_DATA  = os.path.join(os.path.split(__file__)[0],'factions.json')
HS_HHEAD_DATA = os.path.join(os.path.split(__file__)[0],'hearthhead.json')
HS_FACTIONS  = {0:None,1:'Alliance',2:'Horde',3:'Neutral'}

class HearthstoneDataFile(object):

    def __init__(self,pathToFile):

        self.path  = pathToFile
        self.handl = open(self.path)
        self.data  = json.load(self.handl)
        self.types = self.data.keys()
        self.factionpatch = open(HS_FACT_DATA)
        self.factiondata = json.load(self.factionpatch)
        self.hearthheadpatch = open(HS_HHEAD_DATA)
        self.hearthheaddata = json.load(self.hearthheadpatch)
        self.rarities = []
        self.handl.close()

    def _patchCardFaction(self,carddata,id):
        if id in self.factiondata:
            carddata['faction'] = HS_FACTIONS[self.factiondata[id]['faction']]
            
    def iterCards(self):

        for typekey in self.types:
            for carddata in self.data[typekey]:
                cardid   = carddata['id']
                self._patchCardFaction(carddata,cardid)
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
                if 'faction' in carddata:
                    cardfact = carddata['faction']
                else: cardfact = None
                if 'text' in carddata:
                    cardtext = carddata['text']
                else: cardtext = '<em>No text was found for this card.</em>'
                if 'attack' in carddata:
                    cardatk  = carddata['attack']
                else: cardatk = 0
                if 'health' in carddata:
                    carddef  = carddata['health']
                else: carddef = 0
                yield self._makeCard(cardid,cardname,cardcost,cardcoll,cardrarity,cardhero,cardtype,cardfact,cardtext,cardatk,carddef)

    def _makeCard(self,id,name,cost,coll,rarity,hero,type,fact,txt,a,h):
        card = HearthstoneCard(id,name,cost,coll,rarity,hero,type,fact,txt,a,h)
        if id in self.hearthheaddata:
            card.hearthhead_id  = self.hearthheaddata[id]['hearthhead_id' ]
            card.hearthhead_url = self.hearthheaddata[id]['hearthhead_url']
        return card

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
                
    def iterCards(self):
        for type in self.getTypes():
            for card in self.iterCardsForType(type):
                yield card

    def getHeroes(self):    return self.heroes
    def getHeroNames(self): return [x.getHero() for x in self.heroes]


class HearthstoneCard(object):

    def __init__(self,id='',name='',cost=0,collectible=True,rarity='Free',hero=None,type='',faction='',text='',atk=0,hp=0,hh_id=None,hh_url=''):

        self.id = id
        self.name = name
        self.cost = cost
        self.collectible = collectible
        self.rarity = rarity
        self.hero = hero
        self.type = type
        self.faction = faction
        self.text = text
        self.attack = atk
        self.defense = hp
        self.hearthhead_id = hh_id
        self.hearthhead_url = hh_url
        self.goldCard = False

    def getID(self): return self.id
    def getName(self): return self.name
    def getCost(self): return self.cost
    def isCollectible(self): return self.collectible
    def getRarity(self): return self.rarity
    def getType(self): return self.type
    def getHero(self): return self.hero
    def getFaction(self): return self.faction
    def getText(self): return self.text.replace('"',"&quot;")
    def getAttack(self): return self.attack
    def getDefense(self): return self.defense
    def getHearthheadURL(self): return self.hearthhead_url
    def setGoldCard(self,gold): self.goldCard = gold

    def _imgLink(self,size,gold=False):
        
        if self.goldCard or gold: gold_str = '_premium'
        else:                     gold_str = ''
        if size not in ['small','medium','original','animated']:
            raise ValueError('Size provided not defined.')
        if size == 'animated': ext = 'gif'
        else: ext = 'png'
        return 'http://wow.zamimg.com/images/hearthstone/cards/enus/%s/%s%s.%s' % (size,self.id,gold_str,ext)

    def getImgThumbnail(self):
        
        return self._imgLink('small')

    def getImgLink(self):

        return self._imgLink('medium')

    def getFullImgLink(self):
        
        return self._imgLink('original')

    def getAnimatedImgLink(self):
        
        return self._imgLink('animated',True)

    def getPlainStr(self):

        return '%s (%d)' % (self.name,self.cost)

    def toDebugString(self):

        return '[%s:%s:%s] (%d) <For Hero: %s> <Type: %s>' % (self.name,self.rarity,self.id,self.cost,self.hero,self.type)

    def toPlainHTMLString(self):
        
        str = '<span class="rarity_%s">%s</span>' % (self.rarity,self.name)
        if self.getHero() is not None: str = '<span class="card_Spell">' + str + '</span>'
        return str + ' (%d)' % (self.cost)        

    def getUniqueID(self): 

        ''' Uses built-in python function to return a unique integer associated with this instance. '''

        return str(id(self))

    def __eq__(self,x):

        return (x.getID() == self.getID())

    def __ne__(self,x):

        return not self.__eq__(x)

    def __str__(self):

        return self.toPlainHTMLString()