import os
import urllib
import webapp2

from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers

class MainHandler(webapp2.RequestHandler):
  def get(self):
    upload_url = blobstore.create_upload_url('/upload')
    self.response.out.write('<html><body>')
    self.response.out.write('<form action="%s" method="POST" enctype="multipart/form-data">' % upload_url)
    self.response.out.write("""Upload File: <input type="file" name="file"><br> <input type="submit"
        name="submit" value="Submit"> </form></body></html>""")

class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
  def post(self):
    upload_files = self.get_uploads('file')  # 'file' is file upload field in the form
    blob_info = upload_files[0]
    self.redirect('/serve/%s' % blob_info.key())

class ServeHandler(blobstore_handlers.BlobstoreDownloadHandler):
  def get(self, resource):
    resource = str(urllib.unquote(resource))
    blob_info = blobstore.BlobInfo.get(resource)
    self.send_blob(blob_info)


application = webapp2.WSGIApplication([('/load', MainHandler),
                               ('/upload', UploadHandler),
                               ('/serve/([^/]+)?', ServeHandler)],
                              debug=True)

'''
from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
import webapp2
import urllib
import jinja2
import os
import re
import models

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class Upload(webapp2.RequestHandler):
    def get(self):
        store = blobstore.create_upload_url('/storage')
        template_values = {'store': store}
        template = JINJA_ENVIRONMENT.get_template('template/upload.html')
        self.response.write(template.render())
        
class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
  def post(self):
    upload_files = self.get_uploads('file')  # 'file' is file upload field in the form
    blob_info = upload_files[0]
    self.redirect('/serve/%s' % blob_info.key())
    
    template_values = {'message': 'Access to your image via \"http://localhost:8080/serve/%3' % blob_info.key()}
    template = JINJA_ENVIRONMENT.get_template('template/message.html')
    self.response.write(template.render(template_values))
    

class ServeHandler(blobstore_handlers.BlobstoreDownloadHandler):
  def get(self, resource):
    resource = str(urllib.unquote(resource))
    blob_info = blobstore.BlobInfo.get(resource)
    self.send_blob(blob_info)

application = webapp2.WSGIApplication([
    ('/upload', Upload),
    ('/storage', UploadHandler),
    ('/serve/([^/]+)?', ServeHandler),
], debug=True)
'''