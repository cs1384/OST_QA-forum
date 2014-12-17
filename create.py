from google.appengine.api import users
import webapp2
import jinja2
import os
import models

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class createQuestion(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('template/createQuestion.html')
        self.response.write(template.render())
    def post(self):
        title = self.request.get('title')
        content = self.request.get('content')
        if title == '' or content == '':
            template_values = {'message': 'Both title and content cannot be empty!'}
            template = JINJA_ENVIRONMENT.get_template('template/message.html')
            self.response.write(template.render(template_values))
        else:
            question = models.Question()
            question.author = users.get_current_user()
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
            '''
            template_values = {'message': question}
            template = JINJA_ENVIRONMENT.get_template('template/message.html')
            self.response.write(template.render(template_values))
            '''
            
            
class createAnswer(webapp2.RequestHandler):
    def get(self):
        qid = self.request.get('qid')
        # qid = 5988627519635456
        if qid == '':
            self.redirect('/view')
        else:
            qid = int(qid)
            question = models.Question.get_by_id(qid)
            '''
            template_values = {'message': question}
            template = JINJA_ENVIRONMENT.get_template('template/message.html')
            self.response.write(template.render(template_values))
            '''
            template_values = {'question': question}
            template = JINJA_ENVIRONMENT.get_template('template/createAnswer.html')
            self.response.write(template.render(template_values))
            
    def post(self):
        name = self.request.get('name')
        content = self.request.get('content')
        if name == '' or content == '':
            template_values = {'message': 'Both name and content cannot be empty!'}
            template = JINJA_ENVIRONMENT.get_template('template/message.html')
            self.response.write(template.render(template_values))
        else:
            qid = self.request.get('qid')
            question = models.Question.get_by_id(qid)
            answer = models.Answer()
            answer.author = users.get_current_user()
            answer.content = content
            answer.name = name
            answer.qid = int(qid)
            answer.put()
            temp = repr(int(qid))
            url = '/view?qid=' + temp
            self.redirect(url)
            '''
            template_values = {'message': answer}
            template = JINJA_ENVIRONMENT.get_template('template/message.html')
            self.response.write(template.render(template_values))
            '''

application = webapp2.WSGIApplication([
    ('/createq', createQuestion),
    ('/createa', createAnswer),
], debug=True)