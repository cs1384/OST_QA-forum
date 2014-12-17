from google.appengine.api import users
from google.appengine.ext import ndb
import webapp2
import jinja2
import os
import models

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class Delete(webapp2.RequestHandler):
    def get(self):
        qid = self.request.get('qid')
        aid = self.request.get('aid')
        if qid == '' and aid == '':
            template_values = {'message': 'No aid or qid specified'}
            template = JINJA_ENVIRONMENT.get_template('template/message.html')
            self.response.write(template.render(template_values))
        elif qid != '':
            qid = long(qid)
            qid = int(qid)
            user = users.get_current_user()
            question = models.Question.get_by_id(qid)
            if question.author != user:
                template_values = {'message': 'You don\'t have the permission to delete this question' }
                template = JINJA_ENVIRONMENT.get_template('template/message.html')
                self.response.write(template.render(template_values))
            else:
                question.key.delete()
                query = models.Answer.query(models.Answer.qid==question.key.id())
                fetch = query.fetch()
                for answer in fetch:
                    answer.key.delete()
                self.redirect('/view')
        elif aid != '':
            aid = long(aid)
            aid = int(aid)
            user = users.get_current_user()
            answer = models.Answer.get_by_id(aid)
            qid = answer.qid
            if answer.author != user:
                template_values = {'message': 'You don\'t have the permission to delete this answer' }
                template = JINJA_ENVIRONMENT.get_template('template/message.html')
                self.response.write(template.render(template_values))
            else:
                answer.key.delete()
                temp = repr(int(qid))
                self.redirect('/view?qid=' + temp)



application = webapp2.WSGIApplication([
    ('/delete', Delete),
], debug=True)