''' Establishes the plugin system for allowing different game modes for drafting. '''

from modes import * # Get all game modes.
import os, glob

HS_DEFAULT_MODE    = 'arena'
HS_GAME_MODE_PATH  = os.path.join(os.path.split(__file__)[0],'modes')
HS_GAME_MODE_FILES = glob.glob(os.path.join(HS_GAME_MODE_PATH,'*.py'))
HS_GAME_MODES      = [os.path.split(x)[-1].strip('.py') for x in HS_GAME_MODE_FILES
                     if not x.endswith('__init__.py')]

class gameModeContext(object):
    
    def __init__(self,currmode, option):
        self.modes = HS_GAME_MODES
        self.files = HS_GAME_MODE_FILES
        self.currmode = globals()[currmode]
        self.option = option
    
    def getCurrentMode(self): return self.currmode
    def getDefaultMode(self): return globals()[HS_DEFAULT_MODE]
    def getModes(self):
        modes = []
        for m in self.modes: modes.append(globals()[m])
        return modes
    def getOption(self): return self.option

def getMode(mode):
    
    if isMode(mode):
        _mode = globals()[mode]
        return _mode.gameMode
    else: return None

def isMode(mode):
    
    return (mode in HS_GAME_MODES)