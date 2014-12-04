''' Hearthhead Mock API '''

import requests
from lxml import etree as elementTree

class HearthheadCardQuery(object):
  
  def __init__(self,card):
    
    self.card = card
    
  def _getSearchString(self):
    
    searchPrefix = 'http://www.hearthhead.com/search?q='
    cardSearchString = self.card.getName().replace(' ','+')
   
  def _search(self):
    
    searchString = self._getSearchString()
    htmlParse = html.fromstring()