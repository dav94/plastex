import string,re
from plasTeX.Renderers import Renderer
from PageTree import PageTree

class MediaWikiRenderer (Renderer):

    outputType = unicode
    fileExtension = '.xml'
    lineWidth = 76

    aliases = {
        'superscript': 'active::^',
        'subscript': 'active::_',
        'dollar': '$',
        'percent': '%',
        'opencurly': '{',
        'closecurly': '}',
        'underscore': '_',
        'ampersand': '&',
        'hashmark': '#',
        'space': ' ',
        'tilde': 'active::~',
        'at': '@',
        'backslash': '\\',
    }

    def __init__(self, *args, **kwargs):
        Renderer.__init__(self, *args, **kwargs)
        # Load dictionary with methods
        for key in dir(self):
            if key.startswith('do__'):
                self[self.aliases[key[4:]]] = getattr(self, key)
            elif key.startswith('do_'):
                self[key[3:]] = getattr(self, key)

        self['default-layout'] = self['document-layout'] = self.default
        self.footnotes = []
        self.blocks = []
        #tree object
        self.tree = PageTree()
        self.list_level='' 

    def default(self, node):
        s = []
        s.append('<%s>' % node.nodeName)
        s.append(unicode(node))
        s.append('</%s>' % node.nodeName)
        return u''.join(s)


    def do_textDefault(self, node):
        return node 


    #sectioning
    def sectioning(self, node,page_type):
        title = unicode(node.attributes['title'])
        #adding index to parent
        self.tree.addIndexParentPage(title)
        #creation of the new page
        self.tree.createPage(title,page_type)
        #content processing
        text = unicode(node)
        #adding text to current page
        self.tree.addTextCurrentPage(text)
        #exiting the section
        self.tree.exitPage()


    def do_part (self,node):
        self.sectioning(node,'part')
        return u''

    def do_chapter (self,node):
        self.sectioning(node,'chapter')
        return u''

    def do_section(self,node):
        self.sectioning(node,'section')
        return u''

    def do_subsection(self,node):
        self.sectioning(node,'subsection')
        return u''

    def do_equation(self, node):
    	s = []
        s.append('<dmath>')
        #child nodes
        s.append(unicode(node))
        #endtah
        s.append('</dmath>')
        return u''.join(s)
    

    def do_document(self,node):
        content = unicode(node)
        return u'%s' % content

    def do_par(self, node):
        s = []
        s.append(u'\n\n')
        s.append(unicode(node))
        return u''.join(s)
        
    def do_textbf(self,node):
        s=[]
        s.append(u"\'\'\'")
        s.append(unicode(node))
        s.append(u"\'\'\'")
        return u''.join(s)
        
    def do_textit(self,node):
        s=[]
        s.append(u"\'\'")
        s.append(unicode(node))
        s.append(u"\'\'")
        return u''.join(s)    

    do_emph = do_textit
    do_itshape=do_textit
   

    def do__backslash(self,node):
        s = []
        s.append(u'\n')
        s.append(unicode(node))
        return u''.join(s)


    def do_newpage(self,node):
        s = []
        s.append(u'')
        s.append(unicode(node))
        return u''.join(s)

    def do_itemize(self,node):
        s = []
        self.list_level+='*'
        for item in node.childNodes:
            t=unicode(item)
            s.append(self.list_level+t)
        self.list_level = self.list_level[:-1]
        return u'\n'.join(s)

    def do_enumerate(self,node):
        s = []
        self.list_level+='#'
        for item in node.childNodes:
            t=unicode(item)
            s.append(self.list_level+t)
        self.list_level = self.list_level[:-1]
        return u'\n'.join(s)
    
    def do_description(self,node):
        s = []
        for item in node.childNodes:
            t=unicode(item)
            s.append(u';'+ str(item.attributes['term'])+":" +t)
        return u'\n'.join(s)

    def do__tilde(self,node):
        return unicode(node)    

    def do__dollar(self,node):
        s=[]
        return u'$'

    def do__percent(self,node):
        s=[]
        return u'%'

    def do__opencurly(self,node):
        s=[]
        return u'{'

    def do__closecurly(self,node):
        s=[]
        return u'}'
    
    def do__hashmark(self,node):
        s=[]
        return u'#'

    def do__underscore(self,node):
        s=[]
        return u'_'

    def do__ampersand(self,node):
        s=[]
        return u'&'
    
    

class XMLRenderer(Renderer):


    def __init__(self, *args, **kwargs):
        Renderer.__init__(self, *args, **kwargs)
        # Load dictionary with methods
        for key in dir(self):
            if key.startswith('do_'):
                self[key[3:]] = getattr(self, key)
        self['default-layout'] = self['document-layout'] = self.default
        self.footnotes = []
        self.blocks = []
        self['\\']=self.backslash
        
          

    def default(nself,node):
        s = []
        s.append('<%s>' % node.nodeName)
        if node.hasAttributes() :
            s.append('<attributes>')
            for key, value in node.attributes.items():
                if key == 'self':
                    continue
                s.append('<%s>%s</%s>' % (key,unicode(value),key))
            s.append('</attributes>')

        s.append(unicode(node))
        s.append('</%s>\n' % node.nodeName)
        return u'\n'.join(s)

    def textDefault(self,node):
        return unicode(node)

    def backslash(self,node):
        return u"<accapo>"

    def do_math(self, node): #TBD
        s = []
        s.append('<%s>' % node.nodeName)
        return u''
        #return '<math>'+re.sub(r'\s*(_|\^)\s*', r'\1', node.source)+'</math>'

    do_ensuremath = do_math
    
    def do_equation(self, node): #TBD
        s = u'   %s' % re.compile(r'^\s*\S+\s*(.*?)\s*\S+\s*$', re.S).sub(r'\1', node.source)
        return '<math>'+re.sub(r'\s*(_|\^)\s*', r'\1', s)+'</math>'

    

   