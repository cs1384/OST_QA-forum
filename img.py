from google.appengine.api import users
from google.appengine.ext import ndb
import webapp2
import jinja2
import os
import re
import models

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class Img(webapp2.RequestHandler):
    def get(self):
        iid = self.request.get('iid')
        iid = long(iid)
        iid = int(iid)
        image = models.Image.get_by_id(iid)
        if image.blob:
            self.response.headers['Content-Type'] = 'image/*'
            self.response.out.write(image.blob)
        else:
            self.error(404)
        '''
        template_values = {'message': iid}
        template = JINJA_ENVIRONMENT.get_template('template/message.html')
        self.response.write(template.render(template_values))
        '''
application = webapp2.WSGIApplication([
    ('/img', Img),
], debug=True)