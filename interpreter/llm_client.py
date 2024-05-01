from litellm import completion
import os

import re
import json


def talk_to_llm(message, messages):
    response = send_prompt(message, messages)
    messages.append(response)
    response_json = find_json_in_string(response)
    return response_json, messages

def send_prompt(message, messages):
    os.environ["OPENAI_API_KEY"] = "--"
    # os.environ["COHERE_API_KEY"] = "your-cohere-key"
    new_message = { "content": message,"role": "user"}
    messages.append(new_message)

    # openai call
    response = completion(model="gpt-3.5-turbo", messages=messages)

    # cohere call
    return response["choices"][0]["message"]["content"]

def find_json_in_string(large_string):
    # Regular expression pattern to extract JSON-like substrings
    # This will handle nested braces up to four levels deep.
    json_pattern = re.compile(r'\{(?:[^{}]*|\{(?:[^{}]*|\{(?:[^{}]*|\{[^{}]*\})*\})*\})*\}')

    # Find all substrings that look like JSON
    potential_jsons = json_pattern.findall(large_string)

    # Try to parse the JSON strings and collect valid ones
    valid_jsons = []
    for string in potential_jsons:
        try:
            # Parse the JSON string and add it to results if it's valid
            parsed_json = json.loads(string)
            valid_jsons.append(parsed_json)
        except json.JSONDecodeError:
            # If JSON is not valid, just skip it
            continue

    return valid_jsons
