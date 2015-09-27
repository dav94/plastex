''' Class that manages the pages' content '''
class Page(object):

	''' Constructor needs title. Self.index contains the list of the subpages'''
	def __init__(self,title,page_type):
		self.title = title
		self.type = page_type
		self.text = ''
		self.index = []

	def addText(self,text):
		self.text = text


	def addIndex(self, ind):
		self.index.append(ind)