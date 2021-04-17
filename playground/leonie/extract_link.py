import os
import regex
import mdutils
import markdown
from lxml import etree, html
import json
import difflib


## import files
md_files = []
CWD= os.getcwd()
file = open(os.path.join(CWD, "test_test.md"))
text = file.read()
text= text.replace("[_", "[")
text= text.replace("_]", "]")
file.close()


# body_markdown = "This is an [inline link](http://google.com). This is a [non inline link][1]\r\n\r\n  [1]: http://yahoo.com"
body_markdown = text
doc = html.fromstring(markdown.markdown(body_markdown))
link_data = []
chapter = []
for title in doc.xpath('//h2/text()'):
    chapter.append(title)


for link in doc.xpath('//a'):
    data = {
        "link" : link.get('href'),
        "link_text": link.text
    }
    sim_index = 0
    for element in link_data:
        sim= difflib.SequenceMatcher(None,element["link_text"],data["link_text"]).ratio()*100
        if sim > 80:
            sim_index=1
    if sim_index == 0:
        link_data.append(data) 
    #[f(x) for x in sequence if condition]
    
link_all= {
    "chapter": chapter[0],
    "data": link_data
}

with open('chapter_links.json', 'w') as fp:
    json.dump(link_all, fp)

with open('chapter.json', 'w') as fp:
    json.dump(chapter, fp)

print(link_data)