import os
import regex
import difflib
import mdutils
import json
import mammoth

# str1="General principles"
# str2="general principles"
# sim= difflib.SequenceMatcher(None,str1, str2).ratio()*100
# print(sim)

raw ={
    "chapter": "1. Test",
    "data": [{"link": "testest", "link_text": "testestest"}]
}
# print(raw)
# # with open('chapter_links.json', 'w') as file:
# #     json.write(raw)

with open("chapter_links.json", "r+") as file:
    data =[json.load(file)]
    #print(data)
    data.append(raw)
    file.seek(0)
    json.dump(data, file)

# with open("2. Sponsoring, Donations, Memberships.docx", "rb") as docx_file:
#     result = mammoth.convert_to_markdown(docx_file)
#     print(result.value)
# with open("2. Sponsoring, Donations, Memberships.md", "w") as markdown_file:
#     markdown_file.write(result.value)

link_all_1= {
    "chapter": docx_file,
    "data": link_data
    }
link_all_2= {
    "chapter": docx_file,
    "data": link_data
    }

print(link_all_1.append((link_all_2))