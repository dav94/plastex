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

    ###############################
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

    def do_subsubsection(self,node):
        self.sectioning(node,'subsubsection')
        return u''

    def do_paragraph(self,node):
        self.sectioning(node,'paragraph')
        return u''
    ############################
    
    #subparagraph are not node of the section tree
    def do_subparagraph(self,node):
        s =[]
        s.append('\n\'\'\'')
        s.append(unicode(node.attributes['title']))
        s.append('\'\'\'\'')
        s.append(unicode(node))
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
        return u'$'

    def do__percent(self,node):
        return u'%'

    def do__opencurly(self,node):
        return u'{'

    def do__closecurly(self,node):
        return u'}'
    
    def do__hashmark(self,node):
        return u'#'

    def do__underscore(self,node):
        return u'_'

    def do__ampersand(self,node):
        return u'&'

    def do_quotation(self, node):
        s = []
        s.append(u'<blockquote>')
        s.append(unicode(node))
        s.append(u'</blockquote>')
        return u''.join(s)

    def do_centering(self, node):
        s = []
        s.append(u'<div style="text-align:center;">')
        s.append(unicode(node))
        s.append(u'</div>')
        return u''.join(s)

    def do_flushright(self, node):
        s = []
        s.append(u'<div style="text-align:right;">')
        s.append(unicode(node))
        s.append(u'</div>')
        return u''.join(s)

    def do_flushleft(self, node):
        return unicode(node)



    ##########################################
    #Math tags
    def do_equation(self, node): #TBD
        begin_tag = None
        end_Tag = None
        label_tag = None
        structure_label_tag = None

        #search \begin and end \tag
        global_begin_tag = re.search(ur'\\\bbegin\b\{(.*?)\}|\\\(|\\\[', node.source)
        global_end_tag = re.search(ur'\\\bend\b\{(.*?)\}|\\\)|\\\]', node.source)

        #get \begin{tag} and \end{tag}
        if global_begin_tag and global_end_tag:
            begin_tag = global_begin_tag.group(0)
            end_tag = global_end_tag.group(0)

        #search equation tag
        global_label_tag = re.search(ur'\\\blabel\b\{(.*?)\}', node.source)

        if global_label_tag:
            label_tag = global_label_tag.group(1)
            structure_label_tag = global_label_tag.group(0)
        else:
            label_tag = ''
            structure_label_tag = ''

        s = node.source
        s = s.replace(begin_tag, "")
        s = s.replace(end_tag, "")
        s = s.replace(structure_label_tag, "")

        # check if label tag exist. If it does, creates the tag
        if label_tag is not '':
            label_tag = "<label> " + label_tag + " </label>"
        else:
            label_tag = ""

        return '<math>'+ label_tag + s +'</math>'

    do_displaymath = do_equation
    do_enumerate = do_equation
    do_eqnarray = do_equation
    do_matrix = do_equation
    do_array = do_equation

    do_quote=do_quotation
    do_verse=do_quotation

    def do_math(self, node): #TBD
        tag = None

        #search content between $ $
        global_tag = re.search(ur'\$(.*?)\$', node.source)

        #get content between $ $
        if global_tag:
            tag = global_tag.group(1)
        else:
            tag = ''

        s = tag
        return '<math>'+ s +'</math>'
        
    do_ensuremath = do_math
    ###############################################
    
    

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

    def do_centering(self, node):
        s = []
        s.append(u'<div style="text-align:center;">')
        s.append(unicode(node))
        s.append(u'</div>')
        return u''.join(s)

    def do_math(self, node): #TBD
        tag = None

        #search content between $ $
        global_tag = re.search(ur'\$(.*?)\$', node.source)

        #get content between $ $
        if global_tag:
            tag = global_tag.group(1)
        else:
            tag = ''

        s = tag
        return '<math>'+ s +'</math>'

    # def do_displaymath(self, node):
    #     begin_tag = None
    #     end_Tag = None
    #     label_tag = None
    #     structure_label_tag = None

    #     #search \begin,\(,\[ and \end,\),\] tags
    #     global_begin_tag = re.search(ur'\\\bbegin\b\{(.*?)\}|\\\(|\\\[', node.source)
    #     global_end_tag = re.search(ur'\\\bend\b\{(.*?)\}|\\\)|\\\]', node.source)

    #     #get \begin{tag}... and \end{tag}...
    #     if global_begin_tag and global_end_tag:
    #         begin_tag = global_begin_tag.group(0)
    #         end_tag = global_end_tag.group(0)

    #     #search equation tag
    #     global_label_tag = re.search(ur'\\\blabel\b\{(.*?)\}', node.source)

    #     if global_label_tag:
    #         label_tag = global_label_tag.group(1)
    #         structure_label_tag = global_label_tag.group(0)
    #     else:
    #         label_tag = ''
    #         structure_label_tag = ''

    #     s = node.source
    #     s = s.replace(begin_tag, "")
    #     s = s.replace(end_tag, "")
    #     s = s.replace(structure_label_tag, "")

    #     # check if label tag exist. If it does, creates the tag
    #     if label_tag is not '':
    #         label_tag = "<label> " + label_tag + " </label>"
    #     else:
    #         label_tag = ""

    #     return '<math>'+ label_tag + s +'</math>'

    do_ensuremath = do_math

    def do_equation(self, node):
        begin_tag = None
        end_Tag = None
        label_tag = None
        structure_label_tag = None

        #search \begin and end \tag
        global_begin_tag = re.search(ur'\\\bbegin\b\{(.*?)\}|\\\(|\\\[', node.source)
        global_end_tag = re.search(ur'\\\bend\b\{(.*?)\}|\\\)|\\\]', node.source)

        #get \begin{tag} and \end{tag}
        if global_begin_tag and global_end_tag:
            begin_tag = global_begin_tag.group(0)
            end_tag = global_end_tag.group(0)

        #search equation tag
        global_label_tag = re.search(ur'\\\blabel\b\{(.*?)\}', node.source)

        if global_label_tag:
            label_tag = global_label_tag.group(1)
            structure_label_tag = global_label_tag.group(0)
        else:
            label_tag = ''
            structure_label_tag = ''

        s = node.source
        s = s.replace(begin_tag, "")
        s = s.replace(end_tag, "")
        s = s.replace(structure_label_tag, "")

        # check if label tag exist. If it does, creates the tag
        if label_tag is not '':
            label_tag = "<label> " + label_tag + " </label>"
        else:
            label_tag = ""

        return '<math>'+ label_tag + s +'</math>'

    do_displaymath = do_equation
    do_enumerate = do_equation
    do_eqnarray = do_equation
    do_matrix = do_equation
    do_array = do_equation
        
 