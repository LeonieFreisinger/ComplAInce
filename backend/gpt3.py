import openai
from dotenv import load_dotenv
import os
import jsonlines
import json
from datetime import datetime
import logging

from models import Message
from config import (
    GPT3_START_SEQUENCE,
    GPT3_RESTART_SEQUENCE,
    GPT3_CONTEXT,
    GPT3_EXAMPLES,
    GPT3_DOCUMENT_SIZE,
    GPT3_FILE,
    FILE_NAME,
    SUGGESTION_COUNT
)

load_dotenv()

class GPT3():
    def __init__(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def get_answer(self, chatContent):
        logging.debug('Starting get_answer')
        history = chatContent[:-1]
        question = chatContent[-1]
        documents = self._search(question)
        answer = self._completion(question, history, documents[0])
        chatContent.append(answer)
        if documents[0] != '':
            suggestion = self._search_keywords(answer, documents[0].metadata)
            if suggestion:
                chatContent.append(suggestion)
        return chatContent

    def _search(self, question):
        logging.debug('Starting _search')
        try:
            response = openai.Engine('ada').search(
                search_model="ada",
                file=GPT3_FILE,
                query=question.body,
                max_rerank=100,
                return_metadata=True
            )
            # sort by score from high to low
            return sorted(response.data, key=lambda el: el.score, reverse=True)
        except openai.InvalidRequestError:
            logging.warn('No document found...')
            return ['']

    def _completion(self, question, history, document):
        """
        this function ask a question to the gpt3 enigne
        input: 
        question - str
        chat_log - str

        output:s
        story - str

        """
        logging.debug('Starting _completion')
        dialog = ''
        for message in history:
            if message.author == 'user':
                dialog = f'{dialog} {GPT3_START_SEQUENCE} {message.body}'
            elif message.author == 'Chatbot':
                dialog = f'{dialog} {GPT3_RESTART_SEQUENCE} {message.body}'
        if dialog != '':
            dialog += ' '
        # check whether document is available
        if document == '':
            content = ''
        else:
            content = document.text
        prompt_text = f'{GPT3_CONTEXT} ### {content} ### {GPT3_EXAMPLES} \n### {dialog}{GPT3_START_SEQUENCE} {question.body} {GPT3_RESTART_SEQUENCE}'
        response = openai.Completion.create(
            engine="davinci-instruct-beta",
            prompt=prompt_text,
            max_tokens=100,
            temperature=0.1,
            top_p=1,
            n=1,
            stream=False,
            stop=["\n", "<|endoftext|>", "\n\nClient:"],
            echo=False,
            presence_penalty=0.8,
            frequency_penalty=1
        )
        story = response['choices'][0]['text']
        out = Message(
            body=story,
            author='Chatbot',
            timestamp=datetime.now()
        )
        return out

    def _search_keywords(self, query, metadata):
        logging.debug('Starting _search_keywords')
        with open('data/chapter_links.json', 'r') as file:
            chapter_links = json.load(file)['data']

        # remove metadata number
        metadata = metadata.split('-')[0]
        # find in which chapter we are
        chapter_titles = [el['chapter'][:-5] for el in chapter_links]
        if not metadata in chapter_titles:
            logging.warn('Chapter was not found in chapter link list...')
            return False
        index = chapter_titles.index(metadata)
        link_chapter_pair = chapter_links[index]['data']
        if len(link_chapter_pair) == 0:
            logging.warn('No data in chapter of chapter link list...')
            return False
        documents = [el['link_text'] if el['link_text'] != None else '' for el in link_chapter_pair ]

        response = openai.Engine('ada').search(
            search_model="ada",
            documents=documents,
            query=query.body,
            max_rerank=100,
            return_metadata=True
        )
        # sort by score from high to low
        response = sorted(response.data, key=lambda el: el.score, reverse=True)
        print(response[:3])
        best_index = [doc.document for doc in response[:SUGGESTION_COUNT]]

        best_link_chapter_pair = []
        for i in best_index:
            best_link_chapter_pair.append(link_chapter_pair[i])
        
        out = Message(
            author="suggestion",
            body=best_link_chapter_pair,
            timestamp=datetime.now()
        )
        return out

    def convert_and_upload_file(self, filepath):
        """
        Converts plain txt file to jsonl and uploads it to GPT-3
        """
        logging.debug('Starting convert_and_upload_file')
        text_chunk = []
        for raw_name in os.listdir(filepath):
            if raw_name[-4:] != '.txt':
                continue
            
            with open(os.path.join(filepath, raw_name), 'r') as file:
                raw_text = file.read()
                raw_text = raw_text.split(' ')

            # split raw text file to chunks
            text_length = len(raw_text)
            chunk_count = int(text_length / GPT3_DOCUMENT_SIZE)
            cache = 0
            for i in range(1, chunk_count + 1):
                cache_text = ' '.join(raw_text[cache:i * GPT3_DOCUMENT_SIZE])
                cache = i * GPT3_DOCUMENT_SIZE
                text_chunk.append({
                        "text": cache_text,
                        "metadata": f'{raw_name[:-4]}-{i}'
                    })
            text_chunk.append({
                "text": ' '.join(raw_text[cache:]),
                "metadata": f'{raw_name[:-4]}-{chunk_count + 1}'
            })

        # create jsonl file
        jsonl_filepath = os.path.join(filepath, '..', FILE_NAME)
        if os.path.exists(jsonl_filepath):
            os.remove(jsonl_filepath)
        with jsonlines.open(jsonl_filepath, mode='a') as file:
            for chunk in text_chunk:
                file.write(chunk)

        try:
            response = openai.File.create(
                file=open(jsonl_filepath),
                purpose='search'
            )
            print(f'Success, the file id is {response.id}')
        except:
            raise Exception('Something went wrong!')

if __name__ == "__main__":
    # Upload new files
    gpt3 = GPT3()
    gpt3.convert_and_upload_file('./data/raw_txt')