import os
import regex
import mdutils
import markdown
from lxml import etree, html
import json


## import files
md_files = []
CWD= os.getcwd()
file = open(os.path.join(CWD, "test_test.md"))
text = file.read()
file.close()


# body_markdown = "This is an [inline link](http://google.com). This is a [non inline link][1]\r\n\r\n  [1]: http://yahoo.com"
body_markdown = text
doc = html.fromstring(markdown.markdown(body_markdown))
# print(markdown.markdown(body_markdown))
link_data = []
#link_text_data = []
chapter = []
for title in doc.xpath('//h2/text()'):
    data = {
        "title" : title, 
    }
    chapter.append(data)
print(chapter[0])

for link in doc.xpath('//a'):
    data = {
        "link" : link.get('href'),
        "link_text": link.text
    }
    link_data.append(data)

link_all= {
    "chapter": chapter[0],
    "data": link_data
}
    #link_data.append(link.get('href'))
    #link_text_data.append(link.text)
# print(len(link_data), len(link_text_data))    
#dict_links = dict(zip(link_data, link_text_data))
# dict_links = dict(zip(link_data, chapter))
with open('chapter_links.json', 'w') as fp:
    json.dump(link_all, fp)

with open('chapter.json', 'w') as fp:
    json.dump(chapter, fp)
print(chapter)