# main.py
# -------------------------
# Fall 2014; Alex Safatli
# -------------------------
# Webapp interface.

import webapp2, jinja2, os, cgi, hearthstone, json

VERSION = 359
JINJA_ENVIRONMENT = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__)))

class MainPage(webapp2.RequestHandler):
    def get(self):
    
        # Get parameters from form elements.
        hero = cgi.escape(self.request.get('hero'))
                
        # Set values in case of empty input.
        if hero == '' or hero == 'random': hero = None
                        
        # Set dummy object.
        draft = None
        
        # If a type was provided from input...
        if True:
            # Instantiate and provide a draft.
            draft = hearthstone.drafter(preferred_hero=hero)
            hero, draftsets = draft.get()
            
        # Jinja template value and handling.
        template_values = {'draft':draft,'hero':hero,'classes':draft.collection.getHeroNames(),'version':VERSION}
        template = JINJA_ENVIRONMENT.get_template('index.html')
        
        # Write to HTML file.
        self.response.write(template.render(template_values))
        
app = webapp2.WSGIApplication([('/', MainPage)],
                              debug=True)
