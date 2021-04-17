import os
import regex
import mdutils
import markdown
from lxml import etree


md_files = []
CWD= os.getcwd()
file = open(os.path.join(CWD, "test_test.md"))
text = file.read()
# print(text)
file.close()

# href_regex = r'href=[\'"]?([^\'" >]+)'
# urls = regex.findall(href_regex, text)

# print(urls)

    #with open(path) as f:
      #  data = f.read()
# rex = """(?|(?<txt>(?<url>(?:ht|f)tps?://\S+(?<=\P{P})))|\(([^)]+)\)\[(\g<url>)\])"""
# pattern = regex.compile(rex)
matches = regex.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text, overlapped=True)
#print(matches)
# for link in matches:
   #print ("\n ",link)


# text = text.split(' ')
# rex_2'\(.*?\)'

body_markdown = "This is an [inline link](http://google.com). This is a [non inline link][1]\r\n\r\n  [1]: http://yahoo.com"
#body_markdown = text
# print(body_markdown)
md = markdown.markdown(body_markdown)
print(md)
doc = etree.fromstring(md)
#print(doc.xpath('//a')[0].text)
for link in doc.xpath('//a'):
     print(link.text, link.get('href'))