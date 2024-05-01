from logging import Logger
from pathlib import Path
from typing import Dict

from llm_client import talk_to_llm
from type_definitions import StepResult, ObjectiveResult, StepOutput

MAX_MESSAGES: int = 30


def execute_step(step_output: StepOutput) -> str:
    return "This is a test message"


def execute_feedback_loop(main_prompt: str, prompt: str, working_dir: Path) -> ObjectiveResult:
    first_prompt = main_prompt + f"\n{prompt}"
    parsed_json, message_history = talk_to_llm(first_prompt, [])
    status, step_result, message_history = task_loop(parsed_json, message_history, working_dir)
    # need to handle the option of step_result=None
    return ObjectiveResult(objective_status=status, text_output=step_result.text_output,
                           files_map=step_result.files_map)


def task_loop(response_json, message_history, working_dir):
    system_messages_count = 1
    status = response_json[0].get("objective_status", None)
    current_response_from_llm = response_json[0]
    while system_messages_count <= MAX_MESSAGES or status is not None:
        task_input = StepOutput(**current_response_from_llm).task_input
        task_res_with_cwd = task_input.run(working_dir=working_dir)
        response_json, message_history = talk_to_llm(task_res_with_cwd, message_history)
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
    result = execute_feedback_loop(main_prompt, prompt, working_dir, logger)
    prev_res[step_objective] = result
    return result


def main():
    # This function contains the main logic of the program.
    execute_feedback_loop(main_prompt="""
    You are a security researcher in a cyber security company with extensive Python and Docker knowledge. 

You are a worker as part of a process of researching a new security control and integrating it as part of the platform 

You have access to a local Linux environment and you will interact with me to use it and achieve your task. 

You will have the history of our conversation so that you can continue from the last point.

You can ask me to do the following commands:

1. Run command - I will run a shell command in the environment and return the output to you.
2. Send content of file - I will provide you with the contents of a local file
3. Write content to file - I will write the content you provide to a file you ask me to

You will receive a main objective and you can divide to sub objectives if needed. Once you believe you completed an objective, you can do what is needed to decide if the objective was completed or not (for example - ask me for an output of a file that contains the result of the task)

Your response will be in the following structure:

```json
{
	"current_objective": "...",
	"required_task": "" // The task you require me to do, if needed (if not - send null)
	"task_input": {"file_name": "file.txt", "file_content": "..."} // The input of the task, can be one or more variables depending on the task, always an object. 
}
```

Required task can be: run_command, send_file_content, write_content_to_file

Objects are:

{”command”: “ls -l” } - Run command

{”file_name”: “file.txt”} - Send content

{"file_name": "file.txt", "file_content": "..."} - Write content to file

Be sure to use commands like ls, pwd and such to find where you are in case you get stuck.

You are located in /Users/jonathan/Tests/claude/test-repo. Be sure to go back there if you suddenly find yourself in an unfamiliar place by accident (unless that’s part of the task)

Also if you see that you are stuck after 3-4 steps on the same sub task, you can send the following and I will provide you with some input:

{”manual_input”: “required”}

If you think you successfully completed the overall objective you were provided (not a single task), simple send:

 {”objective_status”: “completed”}. 

Do this only once you verified that it was completed successfully

A few more rules:

- In your response, you may add a small text above the JSON with your thoughts, but end of each response will be a ONE SINGLE json according to the instructions, no more

---

Docker research instructions

When you’re testing containers, be sure to note the following:

- If there are multiple output destinations (for example - /code and /tmp), be sure to create local directories that will be mounted to those locations, so that you can later inspect their content,
- In continuation for that - use the —rm command and do not leave containers hanging unless it’s necessary. Run the container with all the relevant mounts and see their output once the container closes.
- Also, do not mount your starting directory straight to the container. As mentioned before, create directories for the container and mount them.
- If you discovered that your Dockerfile was not sufficient, it’s OK to rewrite it and run the container again

---
    """, prompt="""
    Instructions on running Gitleaks:

# Gitleaks Detection Guide\n\n## Overview\nThis guide provides instructions on how to use Gitleaks to detect secrets in a Git repository.\n\n## Requirements\n- Gitleaks binary available in your working directory.\n- A Git repository initialized and containing the files to be scanned.\n\n## Steps\n\n1. **Navigate to your repository:**\n   Ensure you are in the root directory of your Git repository.\n\n2. **Run Gitleaks:**\n   Execute the following command to scan the repository and output the findings in JSON format:\n\n   `bash\\n   ../gitleaks detect --source=. --report-path=../leaks-report.json --report-format=json\\n`   \n\n3. **Review the Report:**\n   After running the command, a `leaks-report.json` file will be generated in the parent directory. This file contains all detected secrets in JSON format.\n\n## Example File Content\n\n- `example-file.txt` content:\n  `\\n  This is a test file containing a secret: AKIAIMNOJVGFDXXXE4OA\\n`  \n\n## Detected Secret\n\n- The scan should detect the AWS credentials and provide details such as the location within the file, the commit hash, and the associated author information.

Your objective is to wrap Gitleaks in a Docker image. In your environment you have: 

- The Gitleaks executable named `gitleaks`
- Docker installed and running

You will use the Ubuntu 22.04 Image.

Your goal is to build a Docker image that upon setting up the container, runs Gitleaks on the `/code` directory. It will then make sure that the output is written to the `/tmp` directory. The image will show the output of Gitleaks if its logs are inspected. 

You will create the image and verify that it works properly. This is the definition of your objective.

Your starting location is /mnt/c/Users/Jonathan/test
    """)


if __name__ == "__main__":
    main()
