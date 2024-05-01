from logging import Logger
from pathlib import Path
from typing import Dict, Optional

from interpreter.llm_client import talk_to_llm
from interpreter.utils import print_tree
from type_definitions import StepResult, ObjectiveResult, StepOutput

MAX_MESSAGES: int = 30


def execute_step(step_output: StepOutput) -> str:
    return "This is a test message"


def execute_feedback_loop(prompt: str, working_dir: str, logger: Logger, model: str) -> ObjectiveResult:
    parsed_json, message_history = talk_to_llm(prompt, [], model)
    status, step_result, message_history = task_loop(parsed_json, message_history, working_dir, model)
    # need to handle the option of step_result=None
    return ObjectiveResult(objective_status=status, text_output=step_result["text_output"],
                           files_map=step_result["files_map"])


def task_loop(response_json, message_history, working_dir, model):
    system_messages_count = 1
    status = response_json[0].get("objective_status", None)
    current_response_from_llm = response_json[0]
    while system_messages_count <= MAX_MESSAGES and status is None:
        print("------------------ Step Start ------------------")
        step_output = StepOutput(**current_response_from_llm)
        task_input = step_output.task_input
        task_res_with_cwd = task_input.run(working_dir=working_dir)
        response_json, message_history = talk_to_llm(task_res_with_cwd, message_history, model)
        print(response_json[0].get("current_objective", None))
        status = response_json[0].get("objective_status", None)
        system_messages_count += 1
        current_response_from_llm = response_json[0]
        print("------------------ Step Finish ------------------")
    print("------------------ Finish Loop ------------------")

    if status is None:
        status = "failed"
        return status, None, message_history
    else:
        print(current_response_from_llm)
        return status, StepResult(**current_response_from_llm), message_history


def run_single_obj(
        objective_prompt: str,
        main_prompt: str,
        research_prompt: str,
        working_dir: Path,
        control_name: str,
        logger: Logger,
        executable_name: Optional[str],
        model: str
) -> ObjectiveResult:
    initial_prompt = main_prompt + research_prompt + f"\n{objective_prompt}" + f"Your starting location is {working_dir} \n" + f"The directory tree is: {print_tree(working_dir)} " + f"You have the {control_name} executable in the current directory named {executable_name}."
    additional_prompt = ""
    if "claude" in model:
        additional_prompt = "\nremember you are only allowed to response with a single json object"
    result = execute_feedback_loop(prompt=initial_prompt + additional_prompt, working_dir=str(working_dir), logger=logger, model=model)
    return result

# def main():
#     # This function contains the main logic of the program.
#     os.chdir("/Users/moshikol/projects/jitathon-control-freaks/interpreter/working_dir")
#     execute_feedback_loop(main_prompt="""
#   ==
#
# intro / persona
#
# You are a security researcher in a cyber security company with extensive Python and Docker knowledge.
#
# You are a worker as part of a process of researching a new security control and integrating it as part of the platform
#
# ==
#
# ==
#
# env + interface
#
# You have access to a mac terminal with docker installed.
#
# You will interact with me to use it and achieve your task.
#
# You will have the history of our conversation so that you can continue from the last point.
#
# You can ask me to do the following commands:
#
# 1. Run command - I will run a shell command in the environment and return the output to you.
# 2. Send content of file - I will provide you with the contents of a local file
# 3. Write content to file - I will write the content you provide to a file you ask me to
#
# You will receive a main objective and you can divide to tasks if needed. Once you believe you completed a task, you can do what is needed to decide if the objective was completed or not (for example - ask me for an output of a file that contains the result of the task)
#
# Your response will be in the following structure:
#
# ```json
# {
# 	"current_objective": "...",
# 	"required_task": "" // The task you require me to do, if needed (if not - send null)
# 	"task_input": {"file_name": "file.txt", "file_content": "..."} // The input of the task, can be one or more variables depending on the task, always an object.
# }
# ```
#
# Required task can be: run_command, send_file_content, write_content_to_file
#
# Valid task input objects are:
#
# {”command”: “ls -l” } - Run command
#
# {”file_name”: “file.txt”} - Send content
#
# {"file_name": "file.txt", "file_content": "..."} - Write content to file
#
# Be sure to use the command ls -lah, in order to find where you are in case you get stuck.
#
# Once you determined that you successfully completed the overall objective you were provided (not a single task), send the following json message:
#
# ```json
#  {
# 	 "objective_status": "completed",
# 	 "text_output": "..Explanation of what was done and what was achieved on the overall objective",
# 	 "files_map": {
# 			 "Dockerfile": "The dockerfile for the container",
# 			 "example.py": "The main Python file that wraps the binary",
# 			 "code/file.txt":"The example file that includes the findings"
#
# 		}
#   }
# ```
#
# In the files map, we expect a list of relevant files that will be transferred to future tasks. You will provide the names of the files you created and for each file a description of what it does and what you did (not the file content). The file names will be the relevant path from the starting directory.
#
# ==
#
# ==
#
# docker instructions
#
# When you’re testing containers, be sure to note the following:
#
# - If there are multiple output destinations (for example - /code and /tmp), be sure to create local directories that will be mounted to those locations, so that you can later inspect their content,
# - In continuation for that - use the —rm command and do not leave containers hanging unless it’s necessary. Run the container with all the relevant mounts and see their output once the container closes.
# - Also, do not mount your starting directory straight to the container. As mentioned before, create directories for the container and mount them.
# - If you discovered that your Dockerfile was not sufficient, it’s OK to rewrite it and run the container again
#
# ==
#
# ==
#
# Important rule
#
# - In your response, you may add a small text above the JSON with your thoughts, but end of each response will be a ONE SINGLE json according to the instructions, no more
# - When you edit an existing file content, I expect you to write to me the entire file content, not just parts to edit - the reason for that is that I take the code as is and override the relevant file content with the code you give me, or else I would not know how to edit it.
#
# ==
#
#     """,
#                           prompt=f"""
#     Our Gitleaks research:
#
# Gitleaks must run in a valid Git repo, otherwise it finds nothing.
#
# Here is the gitleaks help:
#
# ```json
# Gitleaks scans code, past or present, for secrets
#
# Usage:
#   gitleaks [command]
#
# Available Commands:
#   completion  generate the autocompletion script for the specified shell
#   detect      detect secrets in code
#   help        Help about any command
#   protect     protect secrets in code
#   version     display gitleaks version
#
# Flags:
#   -b, --baseline-path string                                                                             path to baseline with issues that can be ignored
#   -c, --config string                                                                                    config file path
#                                                                                                          order of precedence:
#                                                                                                          1. --config/-c
#                                                                                                          2. env var GITLEAKS_CONFIG
#                                                                                                          3. (--source/-s)/.gitleaks.toml
#                                                                                                          If none of the three options are used, then gitleaks will use the default config
#       --enable-rule gitleaks detect --enable-rule=atlassian-api-token --enable-rule=slack-access-token   only enable specific rules by id, ex: gitleaks detect --enable-rule=atlassian-api-token --enable-rule=slack-access-token
#       --exit-code int                                                                                    exit code when leaks have been encountered (default 1)
#       --follow-symlinks                                                                                  scan files that are symlinks to other files
#   -i, --gitleaks-ignore-path string                                                                      path to .gitleaksignore file or folder containing one (default ".")
#   -h, --help                                                                                             help for gitleaks
#       --ignore-gitleaks-allow                                                                            ignore gitleaks:allow comments
#   -l, --log-level string                                                                                 log level (trace, debug, info, warn, error, fatal) (default "info")
#       --log-opts string                                                                                  git log options
#       --max-target-megabytes int                                                                         files larger than this will be skipped
#       --no-banner                                                                                        suppress banner
#       --no-color                                                                                         turn off color for verbose output
#       --redact uint[=100]                                                                                redact secrets from logs and stdout. To redact only parts of the secret just apply a percent value from 0..100. For example --redact=20 (default 100%)
#   -f, --report-format string                                                                             output format (json, csv, junit, sarif) (default "json")
#   -r, --report-path string                                                                               report file
#   -s, --source string                                                                                    path to source (default ".")
#   -v, --verbose                                                                                          show verbose output from scan
#
# Use "gitleaks [command] --help" for more information about a command.
# ```
#
# ---
#
# An example for a secret is: `AKIAIMNOJVGFDXXXE4OA`
#
# Note that to run Gitleaks on a non-git repo, you need to provide the —no-git parameter.
#
# Example of Gitleaks execution:
#
# ```json
# gitleaks detect --verbose --report-format=json --report-path=/tmp/gitleaks-report.json --source=/code --no-git
# ```
# Your starting location is {os.getcwd()}
# The directory tree is: {print_tree(Path(os.getcwd()))}
# You have the Gitleaks executable in the current directory.
# Your objective is to wrap the Control in a Docker image. In your environment you have:
#
# - The Control executable
# - Docker installed and running
#
# You will use the Ubuntu 22.04 Image.
#
# Your goal is to build a Docker image that upon setting up the container, runs the Control on the `/code` directory. It will then make sure that the output is written to the `/tmp` directory. The image will show the output of the Control if its logs are inspected.  You must make sure it works by checking that the docker image properly finds the provided example finding, and that a valid JSON result file is created.
#
# You will create the image and verify that it works properly. This is the definition of your objective.
#
#     """, working_dir=os.getcwd())
#
#
# if __name__ == "__main__":
#     main()
