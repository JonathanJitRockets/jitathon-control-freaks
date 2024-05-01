from typing import Dict, List, Type

import os
from llm_client import talk_to_llm

MAX_MESSAGES: int = 30


def execute_step(task_json) -> str:
    return "This is a test message"


def execute_feedback_loop(main_prompt: str, prompt: str):
    first_prompt = main_prompt + f"\n{prompt}"
    response_json, message_history = talk_to_llm(first_prompt, [])
    system_messages_count = 1
    rec_loop(system_messages_count, response_json, message_history)


def rec_loop(system_messages_count, response_json, message_history):
    while system_messages_count <= MAX_MESSAGES:
        new_message = execute_step(response_json)
        response_json, message_history = talk_to_llm(new_message, message_history)
        system_messages_count += 1
        rec_loop(system_messages_count, response_json, message_history)


def main():
    # This function contains the main logic of the program.
    execute_feedback_loop("", "")


if __name__ == "__main__":
    main()
