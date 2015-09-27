from plasTeX.Renderers.MediaWiki import MediaWikiRenderer as WikiRenderer
from plasTeX.Renderers.MediaWiki import XMLRenderer as XMLRenderer
from plasTeX.TeX import TeX
# Instantiate a TeX processor and parse the input text

f = open('test.tex','r')
text = f.read()
tex2 = TeX()
tex2.ownerDocument.config['files']['split-level'] = -100
tex2.ownerDocument.config['files']['filename'] = 'test.xml'
tex2.input(text)
document2 = tex2.parse()
rend = XMLRenderer()
rend.render(document2)

 
f2 = open('test.tex','r')
text2 = f.read()
tex3 = TeX()
tex3.ownerDocument.config['files']['split-level'] = -100
tex3.ownerDocument.config['files']['filename'] = 'test.mw'
tex3.input(text)
document3 = tex3.parse()
rend = WikiRenderer()
rend.render(document3)
o = open('tree.mw','w')
o.write(str(rend.tree.index))