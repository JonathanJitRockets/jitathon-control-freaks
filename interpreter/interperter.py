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


def execute_feedback_loop(main_prompt: str, prompt: str) -> ObjectiveResult:
    first_prompt = main_prompt + f"\n{prompt}"
    parsed_json, message_history = talk_to_llm(first_prompt, [])
    status, step_result, message_history = task_loop(parsed_json, message_history)
    # need to handle the option of step_result=None
    return ObjectiveResult(objective_status=status, text_output=step_result.text_output, files_map=step_result.files_map)


def task_loop(response_json, message_history):
    system_messages_count = 1
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
        research_prompt: str,
        working_dir: Path,
        control_name: str,
        prev_res: Dict[str, StepResult],
        logger: Logger,
        executable_name: Optional[str],
) -> ObjectiveResult:
    result = execute_feedback_loop(main_prompt, prompt)
    prev_res[step_objective] = result
    return result

def main():
    # This function contains the main logic of the program.
    execute_feedback_loop("", "")


if __name__ == "__main__":
    main()
