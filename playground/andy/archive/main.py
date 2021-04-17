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
        raw_text = [el.strip() for el in raw_text if not 'Page |' in el]
        raw_text = [el.strip() for el in raw_text if not '' == el]
        raw_text = ' '.join(raw_text)
        raw_text = raw_text.split('\\')
        raw_text = ' '.join(raw_text)
        raw_text = raw_text.split('\\')
        raw_text = ' '.join(raw_text)

    with jsonlines.open('harry_potter.jsonl', mode='w') as file:
        content = {
            "text": raw_text
        }
        file.write(content)

def upload_file():
    response = openai.File.create(
        file=open("harry_potter_manual.jsonl"),
        purpose='answers'
    )
    print(response)

def open_harry_potter():
    with jsonlines.open('harry_potter_manual.jsonl') as reader:
        for obj in reader:
            print(obj)

def gifts_test():
    with open('gifts_cleaned.md', 'r') as file:
        text1 = file.read()
    with open('gifts2_cleaned.md', 'r') as file:
        text2 = file.read()
    response = openai.Answer.create(
        model="davinci",
        question="What are gifts?",
        documents=[text1, text2],
        max_tokens=30,
        stop=['\n'],
        n=3,
        temperature=0,
        return_metadata=True,
        examples_context="",
        examples=[["What is the value limit for gifts?", "There are no fixed, uniform value limits for gifts & hospitality and what counts as perfectly acceptable in one country or recipient organization could be absolutely out of the question in another. Every case must be judged on its own individual merits. You need to consider local legal provisions and the rules of the recipient organization first and foremost. And these may well define value limits. You must take particular care in connection with public officials: some countries prohibit their public officials from accepting gifts or hospitality under any circumstances. For more Information see the [Compliance Handbook](https://webbooks.siemens.com/public/LC/chen/index.htm?n=Part-1-Activity-Fields,A.-Anti-Corruption,1.-Gifts-and-Hospitality,1.2.-Types-of-Benefits,1.2.1.-Gifts-and-Meals)"]]
        # examples=[["Are gifts of money allowed?","Gifts of money generally create the appearance of bad faith or impropriety. Therefore, such gifts require the prior written approval of the responsible Compliance Officer. For further information, also about what the term gifts of money covers, see [Compliance Handbook](https://webbooks.siemens.com/public/LC/chen/index.htm?n=Part-1-Activity-Fields,A.-Anti-Corruption,1.-Gifts-and-Hospitality,1.2.-Types-of-Benefits,1.2.1.-Gifts-and-Meals)."]]
    )
    print(response)
    with open('response.txt', 'w') as file:
        file.write(str(response))

if __name__ == "__main__":
    gifts_test()
