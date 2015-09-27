''' Class that manages the pages' content '''
class Page(object):

	''' Constructor needs title. Self.index contains the list of the subpages'''
	def __init__(self,title,page_type,level):
		self.title = title
		self.type = page_type
		self.text = ''
		self.index = []
		self.level = level

	def addText(self,text):
		self.text = text


	def addIndex(self, ind):
		self.index.append(ind)

	''' This method insert the text of subpages in this page if his level is 
	greater than the level parameter.
	It requires the dictionary of pages.'''
	def collapseText(self,level,pages_dict):
		if(self.level<level):
			for subpage in self.index:
				pages_dict[subpage].collapseText(level,pages_dict)
				#the subpages'index is created
				for p in self.index:
					self.text += '\n[['+p+']]'
		else:
			#we have to managed the text
			for subpage in self.index:
				t = pages_dict[subpage].collapseText(level,pages_dict)
				#add text
				self.text+= '\n'+t
			#Creation of current page'title
			title = "="*(level-self.level+1)+self.title+"="*(level-self.level+1)
			self.text = title+ "\n"+ self.text
			#return the text
			return self.text
