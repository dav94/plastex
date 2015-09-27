import re

''' Class that manages the pages' content '''
class Page(object):

	''' Constructor needs title. Self.index contains the list of the subpages'''
	def __init__(self,title,url,page_type,level):
		self.title = title
		self.url = url
		#calculated during collapsing
		self.media_url = ''
		self.type = page_type
		self.text = ''
		'''list of subpages urls'''
		self.index = []
		self.level = level

	def addText(self,text):
		self.text = text


	def addIndex(self, ind):
		self.index.append(ind)

	''' This method insert the text of subpages in this page if his level is 
	greater than the level parameter.
	It requires the dictionary of pages.'''
	def collapseText(self,level,pages_dict,mediaurl_dic,last_url,url_dic):
		if(self.level<level):
			last_url = self.url
			for subpage in self.index:
				pages_dict[subpage].collapseText(level,pages_dict,mediaurl_dic,last_url,url_dic)
				#the subpages'index is created
				for p in self.index:
					self.text += '\n[['+p+']]'
				#saving mediaurl
				self.media_url = self.url
				mediaurl_dic[self.url] = self.media_url
		else:
			if self.level==level: 
				last_url = self.url
				#saving mediawikiurl
				self.media_url= self.url
				mediaurl_dic[self.url] = self.media_url
			else:
				#creation of media-wiki url
				murl = last_url+'#'+self.title
				if murl in url_dic:
					nused = url_dic[murl]
					murl+= '_'+str(nused+1)
					url_dic[murl]+=1
				#saving mediawiki url
				self.media_url= self.murl
				mediaurl_dic[self.url]=murl

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

	'''This method insert the right mediawikiurl in 
	the \ref tags after the collapsing'''
	def fixReferences(self, labels,pages):
		for ref in re.finditer('\\ref{(.*?)}', self.text):
			tag = ref.group(0)
			label = reg.group(1)
			self.text.replace(tag,' ([[' + labels[label] + ']]) ')
		for sub in self.index:
			pages[sub].fixReferences(labels,pages)
			

