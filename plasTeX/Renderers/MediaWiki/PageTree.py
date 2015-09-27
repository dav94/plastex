from Page import Page

''' Class that memorize the pages' structure and content during parsing '''
class PageTree (object):

	''' The constructor requires the document name.
		-self.current handles the working section during parsing.
		-self.current_url handles the current url
		-self.pages is a dictionary of pages. The keys are internal url of pages.
		-self.media_urls is a dictionary internal_url = media_url
		-self.labels is a dictionary for label: label=media_url '''
	def __init__(self, doc_title):
		self.doc_title= doc_title
		self.index = {}
		self.pages = {}
		self.media_urls = {}
		self.labels = {}
		#ROOT PAGE
		self.index[doc_title]={}
		r = Page(doc_title,doc_title,'root',-1)
		self.pages[doc_title]= r

		#indexes
		self.previous=''
		self.previous_url=''
		self.current = doc_title
		self.current_url= doc_title


	''' This method creates a new page and enters 
	in his enviroment setting current variables'''
	def createPage(self, title,page_type):
		newurl = self.current_url+"/"+title
		#finding the right dictionary
		path = unicode(self.current_url).split('/')
		#finding level
		level = len(path)-1
		#create new page	
		p = Page(title,newurl,page_type,level)
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
		return self.media_urls[self.labels[label]]


	''' This method collapse the text contained in subpages 
	in the pages with level > level_min.
	Tin pages with level<level_min is inserted an index of subpages. '''
	def collapseText(self,level_min):
		self.pages[self.doc_title].collapseText(level_min,self.pages,self.media_urls,'',{})
		self.labels[label]= self.media_urls[self.labels[label]]

	'''Method that starts the rendering of refs'''
	def fixReferences(self)
		self.pages[self.doc_title].fixReferences(self.labels)


	