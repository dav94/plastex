from Page import Page

''' Class that memorize the pages' structure and content during parsing '''
class PageTree (object):

	''' The constructor requires the document name.
		self.current handles the working section during parsing.
		self.current_url handles the current url '''
	def __init__(self):
		self.index = {}
		self.pages = {}
		#ROOT PAGE
		self.index['ROOT']={}
		r = Page('ROOT','root')
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
		p = Page(newurl,page_type)
		self.index[self.current][title]={}
		self.pages[newurl].append(p)
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


	def getXML():
		pass

