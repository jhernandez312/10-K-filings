import os
import json
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
import re
from sec_api import ExtractorApi
import project.prompt_utils as prompt_utils
import time


# load the .env file
_ = load_dotenv(find_dotenv())
client = OpenAI(
    api_key = os.environ.get('OPENAI_API_KEY'),
)

model = "gpt-3.5-turbo-0125"
temperature = 0.3
max_tokens = 2096
company = ""

def new_prompt():

    # Load the JSON file
    with open('sec_data.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Convert the dictionary to a string
    json_string = json.dumps(data, indent=4)  # 'indent' is optional but makes the output readable


    #prompts
    system_message = prompt_utils.system_message
    prompt = prompt_utils.generate_prompt(json_string)

    messages=[

        {"role": "system", "content": system_message},
        {"role": "user", "content": prompt}
    ]
    return messages



def get_summary():
    messages = new_prompt()
    completion = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return completion.choices[0].message.content