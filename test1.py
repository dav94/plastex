from plasTeX.Renderers.MediaWiki import MediaWikiRenderer as WikiRenderer
from plasTeX.Renderers.MediaWiki import XMLRenderer as XMLRenderer
from plasTeX.TeX import TeX
# Instantiate a TeX processor and parse the input text
tex = TeX()
tex.ownerDocument.config['files']['split-level'] = -100
tex.ownerDocument.config['files']['filename'] = 'text.mw'
tex.input(r'''
\documentclass{book}
\begin{document}

CiaoCIaoCIao
ciao
\end{document}''')

document = tex.parse()
renderer = WikiRenderer()
renderer.render(document)

f = open('test.tex','r')
text = f.read()
tex2 = TeX()
tex2.ownerDocument.config['files']['split-level'] = -100
tex2.ownerDocument.config['files']['filename'] = 'test.xml'
tex2.input(text)
document2 = tex2.parse()
rend = XMLRenderer()
rend.render(document2)

 
