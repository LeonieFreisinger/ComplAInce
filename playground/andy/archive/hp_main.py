import jsonlines
import openai
from dotenv import load_dotenv
import os

load_dotenv()
openai.api_key = os.getenv('OPENAI_KEY')

def create_book():
    with open('harry_potter_raw.txt', 'r') as file:
        raw_text = file.read()
        raw_text = raw_text.split('\n')
        # sample = Hallo! Wie geht es dir?
        # res = sample.split('!')
        # ["Hallo", " Wie geht es dir?"]
        raw_text = [el.strip() for el in raw_text if not 'Page |' in el]
        # raw_text = []
        # for el in raw_text:
        #   if not 'Page |' in el:
        #       raw_text.append(el.strip())
        raw_text = [el.strip() for el in raw_text if not '' == el]
        raw_text = ' '.join(raw_text)
        raw_text = raw_text.split('\\')
        raw_text = ' '.join(raw_text)
        raw_text = raw_text.split('\\')
        raw_text = ' '.join(raw_text)
        raw_text = raw_text.split(' ')

        text_chunk = []
        cache = []
        for i, word in enumerate(raw_text):
            cache.append(word)
            if i % 1000 == 0:
                text_chunk.append({
                    "text": ' '.join(cache)
                })
                cache = []

    with jsonlines.open('harry_potter.jsonl', mode='a') as file:
        for chunk in text_chunk:
            file.write(chunk)

def upload_file():
    response = openai.File.create(
        file=open("harry_potter.jsonl"),
        purpose='answers'
    )
    print(response)

def open_harry_potter():
    with jsonlines.open('harry_potter_manual.jsonl') as reader:
        for obj in reader:
            print(obj)

if __name__ == "__main__":
    create_book()
    # upload_file()
