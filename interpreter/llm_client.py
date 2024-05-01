from litellm import completion
import os
import re
import json

# this funciton will return this:
#   {
# 	"current_objective": "Retrieve and review the Gitleaks output report",
# 	"required_task": "send_file_content",
# 	"task_input": {
# 		"file_name": "tmp/leaks-report.json"
# 	}
# }
#     or:
# {
    # 	"objective_status": "completed",
    # 	"text_output": "Successfully created and verified a Docker image for running Gitleaks. The Docker image scans a mounted '/code' directory and outputs findings to '/tmp/gitleaks-report.json'. The image was tested with a test secret, which Gitleaks successfully identified and logged in the expected JSON format.",
    # 	"files_map": {
    # 		"Dockerfile": "The Dockerfile for the container, which sets up Ubuntu 22.04, installs necessary packages, copies the Gitleaks executable, and sets the command to run Gitleaks on the '/code' directory with output directed to '/tmp'.",
    # 		"code/example.txt": "The test file containing the AWS secret used to validate the Docker image's functionality.",
    # 		"tmp/gitleaks-report.json": "The output file from Gitleaks containing the findings in JSON format."
# 	}
# }
def talk_to_llm(message, messages):
    response = send_prompt(message, messages)
    messages.append(response)
    res_json = find_json_in_string(response["content"])
    return res_json, messages

def send_prompt(message, messages):
    os.environ["OPENAI_API_KEY"] = "--"
    # os.environ["COHERE_API_KEY"] = "your-cohere-key"
    new_message = { "content": message,"role": "user"}
    messages.append(new_message)

    # openai call
    response = completion(model="gpt-3.5-turbo", messages=messages)
    # cohere call
    return response["choices"][0]["message"]

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

if __name__ == '__main__':
    print(talk_to_llm("Hello", []))