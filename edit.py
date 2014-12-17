from google.appengine.api import users
import webapp2
import jinja2
import os
import models

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class EditQuestion(webapp2.RequestHandler):
    def get(self):
        qid = self.request.get('qid')
        user = users.get_current_user()
        if qid == '':
            template_values = {'message': 'No qid specified!'}
            template = JINJA_ENVIRONMENT.get_template('template/message.html')
            self.response.write(template.render(template_values))
        else:
            qid = long(qid)
            qid = int(qid)
            question = models.Question.get_by_id(qid)
            if question.author != user:
                template_values = {'message': 'You don\'t have the permission to edit this question' }
                template = JINJA_ENVIRONMENT.get_template('template/message.html')
                self.response.write(template.render(template_values))
            else:
                temp = ''
                for s in question.tags:
                    temp = temp + ';' + s
                template_values = {'question': question, 'tags':temp}
                template = JINJA_ENVIRONMENT.get_template('template/editQuestion.html')
                self.response.write(template.render(template_values))
    def post(self):
        qid = self.request.get('qid')
        qid = long(qid)
        qid = int(qid)
        title = self.request.get('title')
        content = self.request.get('content')
        if title == '' or content == '':
            template_values = {'message': 'Both title and content cannot be empty!'}
            template = JINJA_ENVIRONMENT.get_template('template/message.html')
            self.response.write(template.render(template_values))
        else:
            question = models.Question.get_by_id(qid)
            question.title = title
            question.content = content
            temp = self.request.get('tags')
            token = temp.split(";")
            tags = []
            for str in token:
                if str != '':
                    str = str.strip()
                    tags.append(str)
            question.tags = tags
            question.put()
            qid = question.key.id()
            temp = repr(int(qid))
            url = '/view?qid=' + temp
            self.redirect(url)
        
class EditAnswer(webapp2.RequestHandler):
    def get(self):
        aid = self.request.get('aid')
        user = users.get_current_user()
        if aid == '':
            template_values = {'message': 'No aid specified!'}
            template = JINJA_ENVIRONMENT.get_template('template/message.html')
            self.response.write(template.render(template_values))
        else:
            aid = long(aid)
            aid = int(aid)
            answer = models.Answer.get_by_id(aid)
            if answer.author != user:
                template_values = {'message': 'You don\'t have the permission to edit this answer' }
                template = JINJA_ENVIRONMENT.get_template('template/message.html')
                self.response.write(template.render(template_values))
            else:
                qid = answer.qid
                qid = int(qid)
                question = models.Question.get_by_id(qid)
                template_values = {'answer': answer, 'question': question}
                template = JINJA_ENVIRONMENT.get_template('template/editAnswer.html')
                self.response.write(template.render(template_values))
    def post(self):
        aid = self.request.get('aid')
        aid = long(aid)
        aid = int(aid)
        name = self.request.get('name')
        content = self.request.get('content')
        if name == '' or content == '':
            template_values = {'message': 'Both name and content cannot be empty!'}
            template = JINJA_ENVIRONMENT.get_template('template/message.html')
            self.response.write(template.render(template_values))
        else:
            answer = models.Answer.get_by_id(aid)
            answer.name = name
            answer.content = content
            answer.put()
            qid = answer.qid
            temp = repr(int(qid))
            url = '/view?qid=' + temp
            self.redirect(url)
        
        
application = webapp2.WSGIApplication([
    ('/edita', EditAnswer),
    ('/editq', EditQuestion),
], debug=True)