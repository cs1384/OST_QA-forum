from google.appengine.ext import ndb
from google.appengine.ext import blobstore

DEFAULT_PROJECT_NAME = 'default_project'

def myproject_key(project_name=DEFAULT_PROJECT_NAME):
    """Constructs a Datastore key for a project entity with project_name."""
    return ndb.Key('Project', project_name)

# Create your models here.

class Question(ndb.Model):
    # get from the form
    author = ndb.UserProperty()
    title = ndb.StringProperty()
    tags = ndb.JsonProperty()
    content = ndb.TextProperty()
    # default 0 and change it later manually
    vote = ndb.IntegerProperty(default=0)
    voteTracker = ndb.JsonProperty()
    # assign and change manually
    createTime = ndb.DateTimeProperty(auto_now_add=True)
    modifyTime = ndb.DateTimeProperty(auto_now=True)

class Answer(ndb.Model):
    # get from the form
    author = ndb.UserProperty()
    name = ndb.StringProperty()
    content = ndb.TextProperty()
    qid = ndb.IntegerProperty()
    # default 0 and change it later manually
    vote = ndb.IntegerProperty(default=0)
    voteTracker = ndb.JsonProperty()
    # assign and change manually
    createTime = ndb.DateTimeProperty(auto_now_add=True)
    modifyTime = ndb.DateTimeProperty(auto_now=True)


class Image(ndb.Model):
    blob = ndb.BlobProperty(required=True)
    blobKey = ndb.BlobKeyProperty(required=True)
    author = ndb.UserProperty()
    # blobKey = ndb.BlobKeyProperty(required=True)
    servingUrl = ndb.StringProperty()
    createTime = ndb.DateTimeProperty(auto_now_add=True)




# class Review(Document):
# 	location 			= StringField(max_length=256)
# 	description 	= StringField(max_length=1024)
# 	title 				= StringField(max_length=256)
# 	star_rating 	= IntField(default=0)
# 	date					= DateTimeField()

	# meta = {
	# 	'indexes': [
	# 		'location',
	# 		'title',
	# 		'star_rating'
	# 	]
	# }