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


	def collapseText(self,level,pages_dict):
		if(self.level<level):
			for subpage in index:
				pages_dict[subpage].collapseText(level,pages_dict)
		else:
			#we have to managed the text
			if len(index)>0:
				for subpage in index:
					pages_dict[subpage].collapseText(level,pages_dict)
			

