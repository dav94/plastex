from plasTeX.Renderers.MediaWiki import MediaWikiRenderer as WikiRenderer
from plasTeX.Renderers.MediaWiki import XMLRenderer as XMLRenderer
from plasTeX.TeX import TeX
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
# Instantiate a TeX processor and parse the input text

f = open('tex_sources/DispenseStruttura.tex','r')
text = f.read().decode('utf-8')
tex2 = TeX()
tex2.ownerDocument.config['files']['split-level'] = -100
tex2.ownerDocument.config['files']['filename'] = 'test.xml'
tex2.input(text)
document2 = tex2.parse()
rend = XMLRenderer()
rend.render(document2)

 
f2 = open('tex_sources/test2.tex','r')
text2 = f2.read().decode('utf-8')
tex3 = TeX()
tex3.ownerDocument.config['files']['split-level'] = -100
tex3.ownerDocument.config['files']['filename'] = 'test.mww'
tex3.input(text2)
document3 = tex3.parse()
rend = WikiRenderer("Test")
rend.render(document3)
#elaborazione
rend.tree.collapseText(0)
rend.tree.fixReferences()
xml = rend.tree.exportXML()
o = open('test.mw','w')
o.write(xml)

#print(str(rend.tree.index))
for k in rend.tree.pages:
	print(str(rend.tree.pages[k]))
	#print(rend.tree.pages[k].text)