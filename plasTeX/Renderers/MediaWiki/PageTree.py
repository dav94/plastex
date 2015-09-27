from Page import Page

''' Class that memorize the pages' structure and content during parsing '''
class PageTree (object):

	''' The constructor requires the document name.
		self.current handles the working section during parsing.
		self.current_url handles the current url '''
	def __init__(self):
		self.index = {}
		self.pages = {}
		self.label = {}
		#ROOT PAGE
		self.index['ROOT']={}
		r = Page('ROOT','root',-1)
		self.pages['ROOT']= r

		#indexes
		self.previous=''
		self.previous_url=''
		self.current = 'ROOT'
		self.current_url= 'ROOT'


	''' This method creates a new page and enters 
	in his enviroment setting current variables'''
	def createPage(self, title,page_type):
		newurl = self.current_url+"/"+title
		#finding the right dictionary
		path = unicode(self.current_url).split('/')
		#finding level
		level = len(path)-1
		#create new page	
		p = Page(newurl,page_type,level)
		#update index
		cindex = self.index
		for i in range(0,len(path)):
			cindex = cindex[path[i]]
		#now cindex has the current dict
		#and new key is inserted
		cindex[title]={}
		#add pages to pages index
		self.pages[newurl] = p
		#updates current
		self.previous= self.current
		self.previous_url= self.current_url
		self.current= title
		self.current_url= newurl

	'''This method insert text in the current page   '''
	def addTextCurrentPage(self,text):
		self.pages[self.current_url].addText(text)

	'''This method insert a page in the current page's index. It's used when 
 	subsection is encountered'''
	def addIndexParentPage(self,title):
		self.pages[self.current_url].addIndex(self.current_url+'/'+title)

	'''Return to the parent page enviroment'''
	def exitPage(self):
		self.current = self.previous
		self.current_url= self.previous_url

	def addLabel(self,label):
		self.labels[label]= self.current_url

	def getRef(self,label):
		return self.labels[label]


	''' This method collapse the text contained in subpages 
	in the pages with level > level_min.
	Tin pages with level<level_min is inserted an index of subpages. '''
	def collapseText(self,level_min):
		self.pages['ROOT'].collapseText(level_min,self.pages)

	