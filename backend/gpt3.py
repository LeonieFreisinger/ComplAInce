import openai
from dotenv import load_dotenv
import os
import jsonlines

from config import (
    START_SEQUENCE,
    RESTART_SEQUENCE,
    SESSION_PROMPT,
    GPT3_DOCUMENT_SIZE,
    GPT3_FILE,
    FILE_NAME
)

load_dotenv()

class GPT3():
    def __init__(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def get_answer(self, question):
        documents = self._search(question)

    def _search(self, question):
        response = openai.Engine('ada').search(
            search_model="ada",
            file=GPT3_FILE,
            query=question,
            max_rerank=100,
            return_metadata=True
        )
        # sort by score from high to low
        return sorted(response.data, key=lambda el: el.score, reverse=True)

    def ask(self, question, chat_log=None):
        """
        this function ask a question to the gpt3 enigne
        input: 
        question - str
        chat_log - str

        output:s
        story - str

        """
        prompt_text = f'{chat_log}{RESTART_SEQUENCE}{question}{START_SEQUENCE}'
        response = openai.Completion.create(
            engine="davinci",
            prompt=prompt_text,
            temperature=0.8,
            max_tokens=150,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0.3,
            stop=["\n"]
        )
        story = response['choices'][0]['text']
        return str(story)

    def append_interaction_to_chat_log(self, question, answer, chat_log=None):
        """
        this function concatinates the new question and answer to the chatlog
        input: 
        question - str
        answer - str
        chat_log - str

        output:
        response - str

        """
        if chat_log is None: 
            chat_log = SESSION_PROMPT 
        new_chat_log = f'{chat_log}{RESTART_SEQUENCE} {question}{START_SEQUENCE}{answer}'
        return new_chat_log

    def convert_and_upload_file(self, filepath):
        """
        Converts plain txt file to jsonl and uploads it to GPT-3
        """
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
        jsonl_filepath = os.path.join(filepath, FILE_NAME)
        if os.path.exists(jsonl_filepath):
            os.remove(jsonl_filepath)
        with jsonlines.open(jsonl_filepath, mode='a') as file:
            for chunk in text_chunk:
                file.write(chunk)

        try:
            openai.File.create(
                file=open(jsonl_filepath),
                purpose='search'
            )
            print('Success')
        except:
            raise Exception('Something went wrong!')

if __name__ == "__main__":
    ## execution
    # chat_log = SESSION_PROMPT
    # question_1 = "Who are you?"
    # print("question_1: ",question_1)
    # answer_1 = ask (question_1, chat_log)
    # print("answer1: ",answer_1)
    # chat_log = append_interaction_to_chat_log(question_1, answer_1, chat_log)
    # #print(chat_log)
    # question_2 = "What is your daily routine?"
    # print("question_2: ",question_2)
    # answer_2 = ask (question_2, chat_log)
    # print("answer2: ",answer_2)
    # chat_log = append_interaction_to_chat_log(question_2, answer_2, chat_log)
    gpt3 = GPT3()
    # gpt3.convert_and_upload_file('./data/raw')
    documents = gpt3.get_answer('I want to send a gift to one of our clients. Is this allowed?')
    print(documents)