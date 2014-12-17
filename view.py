import webapp2
import jinja2
import os
import models
import re

NUM_IN_A_PAGE = 10

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class View(webapp2.RequestHandler):
    def get(self):
        qid = self.request.get('qid')
        if qid == '':
            self.viewAll()
        else:
            self.viewAQ(qid)
    def viewAll(self):
        tag = self.request.get('tag')
        query = models.Question.query().order(-models.Question.modifyTime)
        fetch = query.fetch()
        qs = []
        if tag != '':
            for q in fetch:
                if tag in q.tags:
                    qs.append(q)
        else:
            qs = fetch
        page = self.request.get('page')
        if page == '':
            page = 1
        else:
            page = int(page)
        
        num = len(qs)
        max = int(page) * NUM_IN_A_PAGE
        if max >= num:
            next = -1
            show = qs[(max-10):num]
        else:
            next = int(page) + 1
            show = qs[(max-10):max]
        
        # show = qs
        # temp = show[0].key.id()
        '''
        template_values = {'message': tag}
        template = JINJA_ENVIRONMENT.get_template('template/message.html')
        self.response.write(template.render(template_values))
        '''
        template_values = {'next': next, 'page': page, 'questions': show, 'tag':tag}
        template = JINJA_ENVIRONMENT.get_template('template/viewAll.html')
        self.response.write(template.render(template_values))
        
    def viewAQ(self, qid):
        qid = long(qid)
        qid = int(qid)
        question = models.Question.get_by_id(qid)
        qcontent = self.processContent(question.content)
        # question = models.Question.get_by_id(6410839984701440)
        query = models.Answer.query(models.Answer.qid==qid)
        fetch = query.fetch()
        show = sorted(fetch,key=lambda x: abs(x.vote),reverse=True)
        acontent = []
        for ans in show:
            acontent.append(self.processContent(ans.content))
        
        template_values = {'question': question, 'answers':show, 'qcontent': qcontent, 'acontent': acontent}
        template = JINJA_ENVIRONMENT.get_template('template/viewAQ.html')
        self.response.write(template.render(template_values))
        '''
        template_values = {'message': qcontent}
        template = JINJA_ENVIRONMENT.get_template('template/message.html')
        self.response.write(template.render(template_values))
        '''
        
    
    def processContent(self, content):
        images = re.findall(r"(https?://[^\s]*\.jpg|https?://[^\s]*\.png|https?://[^\s]*\.gif)",content)
        for i in images:
            # print i
            replace = ' <img src="'+ i + '"/> '
            # print replace
            content = content.replace(' '+i+' ',replace)
        links = re.findall(r"https?://[^\s]*\.[^\s\"]*",content)
        for l in links:
            if l not in images:
                replace = ' <a href="'+ l + '">' + l + '</a> '
                # print l
                # print replace
                content = content.replace(' '+l+' ',replace)
        return content
        
            
        
    
    
application = webapp2.WSGIApplication([
    ('/view', View),
    ('/', View),
], debug=True)