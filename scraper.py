''' Scraper for Hearthhead web interface in order to acquire card information and image information. Saves resulting information to a JSON object in order for the web application to associate all cards with a Hearthhead-specific ID. '''

# Date: Sun Jan 18 2015
# Author: Alex Safatli
# Email: safatli@cs.dal.ca

HH_JSON_OUT = 'hearthhead.json'
HH_CARDS_URL = 'http://hearthhead.com/cards'
HH_CARD_URL = 'http://hearthhead.com/card='
HH_CARD_TYPES = {3:'Hero',4:'Minion',5:'Spell',7:'Weapon',10:'Hero Power'}
HH_CARD_CLASSES = {1:'Warrior',2:'Paladin',3:'Hunter',4:'Rogue',5:'Priest',7:'Shaman',8:'Mage',9:'Warlock',11:'Druid'}
HH_CARD_RARITIES = {0:'Free',1:'Common',3:'Rare',4:'Epic',5:'Legendary'}

from bs4 import BeautifulSoup
import urllib2 as urllib, demjson

class hearthheadScraper(object):
    
    page   = HH_CARDS_URL
    url    = None
    parser = None
    raw    = None
    json   = None
    
    def __init__(self):
        
        self.url = urllib.urlopen(HH_CARDS_URL).read()
        self.parser = BeautifulSoup(self.url)
        self.parser.prettify()
        
    def _writeCardData(self):
        
        self.json = {}
        for card in self.raw:
            carddict = {}
            carddict['name'] = card['name']
            carddict['hearthhead_id'] = card['id']
            carddict['id'] = card['image']
            carddict['hearthhead_url'] = HH_CARD_URL + str(card['id'])
            self.json[carddict['id']] = carddict
        out = demjson.encode(self.json)
        o = open(HH_JSON_OUT,'w')
        o.write(out)
        o.close()
        
    def scrape(self):
        
        parser = self.parser
        hcards = parser.find('div',id='lv-hearthstonecards')
        scriptdata = hcards.findNext('script')
        if not (scriptdata):
            raise IOError('Could not find proper JavaScript element in Hearthhead.')
        # Extract variable data from the raw script code.
        rawscript = scriptdata.text.split('hearthstoneCards')[1].split('[')[1].split(']')[0]
        # Validate and reformat the JSON, parsing it as a list of dictionaries.
        rawcards  = demjson.decode("[" + rawscript + "]")
        # Store into the object.
        self.raw  = rawcards
        self._writeCardData()
        
if __name__ == '__main__':
    # No imports.
    h = hearthheadScraper()
    h.scrape()
    print 'Scraping completed successfully. %d cards retrieved.' % (len(h.raw))
        
        
    
    
        
