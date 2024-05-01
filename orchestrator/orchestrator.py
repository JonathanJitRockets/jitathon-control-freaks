import json
import os
import shutil
import tempfile
from logging import Logger
from pathlib import Path
from typing import Iterable, Optional
from uuid import uuid4

from interpreter.interperter import run_single_obj
from type_definitions import OrchestrationInstructions, StepResult


def write_result_files_to_dir(result: Iterable[StepResult], working_dir: Path) -> None:
    for step_result in result:
        for file_name, file_contents in step_result["files_map"].items():
            try:
                os.mkdir((working_dir / file_name).parent)
            except FileExistsError:
                pass
            with open(working_dir / file_name, "w") as file:
                file.write(file_contents)


def write_research_files_to_dir(research_files: list[str], working_dir: Path) -> None:
    for file_path in research_files:
        shutil.copy(file_path, working_dir)


def orchestrate(orchestration_instructions: OrchestrationInstructions) -> None:
    logger = Logger("orchestrator")
    logger.info("Beginning control creation orchestration")
    workflow_id = str(uuid4())
    workflows_dir = "workflows"
    os.mkdir(f'{workflows_dir}/{workflow_id}')
    working_directory = f'{workflows_dir}/{workflow_id}'
    results = {}
    for index, step in enumerate(orchestration_instructions["step_instructions"]):
        logger.info(f"Running step #{index + 1}: {step['step_objective']}")
        step_directory = Path(working_directory.name) / f"step_{index + 1}"
        step_directory.mkdir()
        write_result_files_to_dir(results.values(), step_directory)
        write_research_files_to_dir(
            orchestration_instructions["research_files"], step_directory)
        objective_result = run_single_obj(
            objective_prompt=step["step_prompt"],
            main_prompt=orchestration_instructions["main_prompt"],
            research_prompt=orchestration_instructions["research_prompt"],
            control_name=orchestration_instructions["control_name"],
            working_dir=step_directory,
            logger=logger,
            executable_name=orchestration_instructions["executable_name"],
            model=step["model"]
        )
        if objective_result["objective_status"] == "failed":
            logger.error(f"Objective failed: {step['step_objective']}")
            return
        logger.info(f"Step #{index + 1} complete: {step['step_objective']}")
        results[step["step_objective"]] = objective_result
    logger.info("Control creation orchestration complete")
    logger.info(f"Results dir: {working_directory}")
    # working_directory.cleanup()


def main(
        instructions_path: str,
        research_prompt: str,
        control_name: str,
        research_files: Optional[list[str]] = None,
        executable_name: Optional[str] = None,
) -> None:
    with open(instructions_path, "r") as instructions_file:
        orchestration_instructions: OrchestrationInstructions = json.load(
            instructions_file)
    research_files: list[str] = research_files or []
    orchestrate({
        "main_prompt": orchestration_instructions["main_prompt"],
        "step_instructions": orchestration_instructions["step_instructions"],
        "research_prompt": research_prompt,
        "research_files": research_files,
        "control_name": control_name,
        "executable_name": executable_name,
    })


if __name__ == '__main__':
    base_dir = Path(__file__).parent.parent / 'inputs'
    main(str(base_dir / "instructions.json"),
         (base_dir / "research_prompt.txt").read_text(),
         "gitleaks",
         [str(base_dir / "gitleaks")],
         executable_name="gitleaks",
         )
