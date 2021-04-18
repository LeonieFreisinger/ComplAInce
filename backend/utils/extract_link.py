import os
import regex
import mdutils
import markdown
from lxml import etree, html
import json
import difflib
import mammoth
#import pandoc

#variables
sim_val = 80
min_link_text_len = int(4)

def convert_doc_to_txt(filepath, docx_file):
    with open(os.path.join(filepath, docx_file), "rb") as docx_file:
        result = mammoth.convert_to_markdown(docx_file)
    text = result.value
    text= text.replace("[_", "[")
    text= text.replace("_]", "]")   
   # text= text.replace("&quot;", " ")  
    #text= text.replace("\u00fc;", "ü")   
   # text= text.replace("\u00f6;", "ö") 
    #text= text.replace("\u00a0;", " ")   
    #text= text.replace("\u00b4;", "`") 
    return text
  

def extract_link_to_json(text, docx_file):
    doc = html.fromstring(markdown.markdown(text))
    link_data = []
    chapter = []

    for link in doc.xpath('//a'):
        data = {
        "link" : link.get('href'),
        "link_text": link.text
        }
        # print(data)
        if data["link"] is None or data["link_text"] is None:
            continue
        sim_index = 0
        for element in link_data:
            sim= difflib.SequenceMatcher(None,element["link_text"],data["link_text"]).ratio()*100
            if sim > sim_val:
                sim_index=1
        if sim_index == 0 and len(data["link_text"])> min_link_text_len:
            link_data.append(data)
   
    link_all= {
    "chapter": docx_file,
    "data": link_data
    }

    with open("chapter_links.json", "r+") as file:
        data = json.load(file)
        data['data'].append(link_all)
        file.seek(0)
        json.dump(data, file)    

         

filepath = ('../data/docx')
if os.path.exists('chapter_links.json'):
    os.remove('chapter_links.json')
with open('chapter_links.json', 'w') as file:
    json.dump({
        "data": []
    }, file)
for docx_file in os.listdir(filepath):
    #print(docx_file)
    text = convert_doc_to_txt(filepath, docx_file)
    extract_link_to_json(text, docx_file)
    print("test")   
                