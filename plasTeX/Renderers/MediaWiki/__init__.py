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

    def default(self, node):
        s = []
        s.append('<%s>' % node.nodeName)
        s.append(unicode(node))
        s.append('</%s>' % node.nodeName)
        return u''.join(s)


    def do_textDefault(self, node):
        return node 


    #sectioning
    def do_section(self,node):
        title = node.attributes['title']
        #adding index to parent
        self.tree.addIndexParentPage(title)
        #creation of the new page
        self.tree.createPage(title,'section')
        #content processing
        text = unicode(node)
        #adding text to current page
        self.tree.addTextCurrentPage(text)
        #exiting the section
        self.tree.exitPage()
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

    # def do_label(self,node):
    #     s = []
    #     s.append(u'<%s>' % node.nodeName)
    #     s.append(unicode(node))
    #     s.append(u'</%s>' % node.nodeName)
    #     return u''.join(s)

    def do_math(self, node): #TBD
        #s = []
        #s.append('<%s>' % node.nodeName)
        #for key, value in node.attributes.items():
        return '<math>'+re.sub(r'\s*(_|\^)\s*', r'\1', node.source)+'</math>'

    do_ensuremath = do_math



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