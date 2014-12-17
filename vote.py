from google.appengine.api import users
import webapp2
import jinja2
import os
import models

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class Vote(webapp2.RequestHandler):
    def get(self):
        aid = self.request.get('aid')
        qid = self.request.get('qid')
        vote = self.request.get('eval')
        if aid != '':
            self.voteAnswer(aid, vote)
        if qid != '':
            self.voteQuestion(qid, vote)
    def voteAnswer(self,aid, vote):
        aid = long(aid)       
        aid = int(aid)
        user = users.get_current_user()
        uid = user.user_id()
        answer = models.Answer.get_by_id(aid)
        if vote == 'up':
            if answer.voteTracker == None:
                answer.voteTracker = {}
            if uid not in answer.voteTracker:
                answer.voteTracker[uid] = 1
                answer.vote = answer.vote + 1
            elif answer.voteTracker[uid] == -1:
                answer.voteTracker[uid] = 1
                answer.vote = answer.vote + 2
        elif vote == 'down':
            if answer.voteTracker == None:
                answer.voteTracker = {}
            if uid not in answer.voteTracker:
                answer.voteTracker[uid] = -1
                answer.vote = answer.vote - 1
            elif answer.voteTracker[uid] == 1:
                answer.voteTracker[uid] = -1
                answer.vote = answer.vote - 2
        elif vote == 'cancel':
            if answer.voteTracker == None:
                answer.voteTracker = {}
            if uid in answer.voteTracker:
                answer.vote = answer.vote - answer.voteTracker[uid]
        answer.put()
        '''
        template_values = {'message': answer }
        template = JINJA_ENVIRONMENT.get_template('template/message.html')
        self.response.write(template.render(template_values))
        '''
        self.redirect('/view?qid='+str(answer.qid))
    
    def voteQuestion(self,qid, vote):
        qid = long(qid)
        qid = int(qid)
        user = users.get_current_user()
        uid = user.user_id()
        question = models.Question.get_by_id(qid)
        if vote == 'up':
            if question.voteTracker == None:
                question.voteTracker = {}
            if uid not in question.voteTracker:
                question.voteTracker[uid] = 1
                question.vote = question.vote + 1
            elif question.voteTracker[uid] == -1:
                question.voteTracker[uid] = 1
                question.vote = question.vote + 2
        elif vote == 'down':
            if question.voteTracker == None:
                question.voteTracker = {}
            if uid not in question.voteTracker:
                question.voteTracker[uid] = -1
                question.vote = question.vote - 1
            elif question.voteTracker[uid] == 1:
                question.voteTracker[uid] = -1
                question.vote = question.vote - 2
        elif vote == 'cancel':
            if question.voteTracker == None:
                question.voteTracker = {}
            if uid in question.voteTracker:
                question.vote = question.vote - question.voteTracker[uid]
                del question.voteTracker[uid]
        question.put()
        '''
        template_values = {'message': answer }
        template = JINJA_ENVIRONMENT.get_template('template/message.html')
        self.response.write(template.render(template_values))
        '''
        self.redirect('/view?qid='+str(question.key.id()))

application = webapp2.WSGIApplication([
    ('/vote', Vote),
], debug=True)