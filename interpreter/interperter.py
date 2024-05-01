from typing import Dict, Optional, List, Type

from type_definitions import StepResult, ObjectiveResult, StepOutput
import os
from llm_client import talk_to_llm
from pathlib import Path
from typing import Dict
from logging import Logger

MAX_MESSAGES: int = 30

def execute_step(step_output: StepOutput) -> str:
    return "This is a test message"


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
def execute_feedback_loop(main_prompt: str, prompt: str) -> ObjectiveResult:
    first_prompt = main_prompt + f"\n{prompt}"
    parsed_json, message_history = talk_to_llm(first_prompt, [])
    system_messages_count = 1
    status, step_result, message_history = loop(system_messages_count, parsed_json, message_history)
    return ObjectiveResult(objective_status=status, text_output=step_result.text_output, files_map=step_result.files_map)


def loop(system_messages_count, response_json, message_history):
    status = response_json.get("objective_status", None)
    while system_messages_count <= MAX_MESSAGES or status is not None:
        new_message = execute_step(StepOutput(**response_json))
        response_json, message_history = talk_to_llm(new_message, message_history)
        status = response_json.get("objective_status", None)
        system_messages_count += 1

    if status is None:
        status = "failed"
        return status, None, message_history
    else:
        return status, StepResult(**response_json), message_history




def run_single_obj(
        step_objective: str,
        prompt: str,
        main_prompt: str,
        working_dir: Path,
        prev_res: Dict[str, StepResult],
        logger: Logger
) -> ObjectiveResult:
    result = execute_feedback_loop(main_prompt, prompt)
    prev_res[step_objective] = result
    return result

def main():
    # This function contains the main logic of the program.
    execute_feedback_loop("", "")


if __name__ == "__main__":
    main()