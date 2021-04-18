from bs4 import BeautifulSoup
from markdown import markdown
import re
import os

def markdown_to_text(markdown_string):
    """ Converts a markdown string to plaintext """

    # md -> html -> text since BeautifulSoup can extract text cleanly
    html = markdown(markdown_string)

    # remove code snippets
    html = re.sub(r'<pre>(.*?)</pre>', ' ', html)
    html = re.sub(r'<code>(.*?)</code >', ' ', html)

    # extract text
    soup = BeautifulSoup(html, "html.parser")
    text = ''.join(soup.findAll(text=True))

    return text

def clean_up(raw):
    raw = raw.split('\n')
    raw = [el for el in raw if not el == '']
    # remove all headlines
    raw = [el for el in raw if not el[0] == '#']
    raw = ' '.join(raw)
    raw = markdown_to_text(raw)
    raw = raw.split('&quot;')
    raw = ' '.join(raw)
    raw = raw.split('\&39;')
    raw = '\''.join(raw)
    raw = re.sub(r"(?:__|[*#])|\[(.*?)\]\(.*?\)", '', raw)
    raw = raw.split('|')
    raw = ''.join(raw)
    raw = raw.split('---')
    raw = ''.join(raw)
    raw = raw.split('_')
    raw = ' '.join(raw)
    raw = raw.split('"')
    raw = ''.join(raw)
    raw = raw.split(' ')
    raw = [el for el in raw if not el == '']
    raw = ' '.join(raw)
    raw = raw.split('\\')
    raw = ''.join(raw)
    return raw

if __name__ == '__main__':
    raw_md = '../data/raw_md'
    raw_txt = '../data/raw_txt'
    for filename in os.listdir(raw_md):
        filename = filename[:-3]
        with open(os.path.join(raw_md, f'{filename}.md'), 'r') as file:
            raw = file.read()

        raw = clean_up(raw)

        with open(os.path.join(raw_txt, f'{filename}.txt'), 'w') as file:
            file.write(raw)