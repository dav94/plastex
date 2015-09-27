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

    def __init__(self, doc_title,*args, **kwargs):
        Renderer.__init__(self, *args, **kwargs)
        #document title
        self.doc_title = doc_title
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
        self.tree = PageTree(doc_title)
        #parameter for list formatting
        self.list_level='' 
        #set for default tags
        self.def_tags = set()

    def default(self, node):
        s = []
        self.def_tags.add(node.nodeName)
        s.append(unicode(node))
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
    #################################################
    
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
        self.tree.addTextCurrentPage(content)
        return u'%s' % content


    ###############################################
    #references
    ''' Method that insert label into PageTree'''
    def label(self,lab):
        #the reference to the current page is saved
        self.tree.addLabel(lab)

    ''' Labels are managed bey PageTree'''
    def do_label(self,node):
        #retriving label id
        l = node.attributes['label']
        self.label(l)

    def do_ref(self,node):
        r = node.attributes['label']
        return unicode(' (\ref{'+r+'}) ')

    do_pageref = do_ref
    do_vref = do_ref


    ################################################
    #Formatting
    def do_par(self, node):
        s = []
        s.append(u'\n')
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
    do_itshape = do_textit
    do_textsl = do_textit
    do_slshape = do_textit
   
    def do_newline(self,node):
        s = []
        s.append(u'\n')
        s.append(unicode(node))
        return u''.join(s)
    
    do__backslash=do_newline

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

    do_quote=do_quotation
    do_verse=do_quotation

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

    def do_footnote(self,node):
        s=[]
        s.append(u" (")
        s.append(unicode(node))
        s.append(u") ")
        return u''.join(s)

    def do_hrulefill(self,node):
        return u'-----'  

    do_rule=do_hrulefill   

    def do_textrm(self, node):
        return unicode(node)

    def do_small(self, node):
        s = []
        s.append(u'<small>')
        s.append(unicode(node))
        s.append(u'</small>')
        return u''.join(s)

    do_tiny=do_small
    do_scriptsize=do_small
    
    def do_underline(self, node):
        s = []
        s.append(u'<u>')
        s.append(unicode(node))
        s.append(u'</u>')
        return u''.join(s)
    
    do_underbar=do_underline

    def do_texttt(self,node):
        s=[]
        s.append(u"<tt>")
        s.append(unicode(node))
        s.append(u"</tt>")
        return u''.join(s)  
        
    ##########################################
    #Image tags

    def do_includegraphics(self,node):
        s = []
        s.append('[[')
        if node.hasAttributes():
            for key, value in node.attributes.items():
                if key == 'self':
                     continue
                if key == 'file':
                    s.append('%s|%s]]' % (unicode(value),unicode(node.parentNode.parentNode.previousSibling.lastChild)))
        return u''.join(s) 

    ###################################################
    #Math tags
    def do_equation(self, node): #TBD
        begin_tag = None
        end_Tag = None
        label_tag = None
        structure_label_tag = None
        s = node.source

        #$$ search
        global_dollars_search = re.search(ur'\$\$(.*?)\$\$', node.source)

        #search \begin and end \tag
        global_begin_tag = re.search(ur'\\\bbegin\b\{(.*?)\}|\\\[', node.source)
        global_end_tag = re.search(ur'\\\bend\b\{(.*?)\}|\\\]', node.source)

        #get content between $$ $$
        #get \begin{tag} and \end{tag}
        if global_begin_tag and global_end_tag:
            begin_tag = global_begin_tag.group(0)
            end_tag = global_end_tag.group(0)
            s = s.replace(begin_tag, "")
            s = s.replace(end_tag, "")
        elif global_dollars_search
            dollars_tag = global_dollars_search.group(1)
            s = s.replace(dollars_tag, "")

        #search equation tag
        global_label_tag = re.search(ur'\\\blabel\b\{(.*?)\}', node.source)

        if global_label_tag:
            label_tag = global_label_tag.group(1)
            structure_label_tag = global_label_tag.group(0)
        else:
            label_tag = ''
            structure_label_tag = ''

        s = s.replace(structure_label_tag, "")

        # check if label tag exist. If it does, creates the tag
        if label_tag is not '':
            label_tag = "<label> " + label_tag + " </label>"
        else:
            label_tag = ""

        #adding label to tree
        self.label(label_tag)
        return '<dmath>'+ label_tag + s +'</dmath>'

    do_displaymath = do_equation
    do_eqnarray = do_equation
    do_matrix = do_equation
    do_array = do_equation
    do_align = do_equation

    def do_math(self, node):
        tag = None

        #search content between $ $
        global_tag = re.search(ur'\$(.*?)\$', node.source)
        
        regexp_brackets_global_tag = re.compile(ur'\\\((.*?)\\\)', re.DOTALL)
        brackets_global_tag = re.search(regexp_brackets_global_tag, node.source)

        #get content between $ $
        if global_tag:
            tag = global_tag.group(1)
        elif brackets_global_tag:
            tag = brackets_global_tag.group(1)
        else:
            tag = ''

        return '<math>'+ tag +'</math>'

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
        
    def do_caption(self,node):
        s = []
        s.append("|")
        s.append(unicode(node))
        return u''.join(s)

    def do_includegraphics(self,node):
        s = []
        s.append('[[')
        if node.hasAttributes():
            for key, value in node.attributes.items():
                if key == 'self':
                     continue
                if key == 'file':
                    s.append('%s|%s]]' % (unicode(value),unicode(node.parentNode.parentNode.previousSibling.lastChild)))
        return u''.join(s) 

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

      


   
