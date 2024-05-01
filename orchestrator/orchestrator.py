import json
import tempfile
from pathlib import Path
from typing import Dict

from type_definitions import ObjectiveResult, OrchestrationInstructions, StepResult
from logging import Logger


def run_single_obj(
        step_objective: str,
        prompt: str,
        main_prompt: str,
        working_dir: Path,
        prev_res: Dict[str, StepResult],
        logger: Logger
) -> ObjectiveResult:
    pass


def orchestrate(orchestration_instructions: OrchestrationInstructions) -> None:
    logger = Logger("orchestrator")
    logger.info("Beginning control creation orchestration")
    working_directory = Path(tempfile.TemporaryDirectory().name)
    results = {}
    for index, step in enumerate(orchestration_instructions["step_instructions"]):
        logger.info(f"Running step #{index + 1}: {step['step_objective']}")
        step_directory = working_directory / f"step_{index + 1}"
        step_directory.mkdir()
        objective_result = run_single_obj(
            step_objective=step["step_objective"],
            prompt=step["step_prompt"],
            main_prompt=orchestration_instructions["main_prompt"],
            working_dir=step_directory,
            prev_res=results,
            logger=logger
        )
        if objective_result["objective_status"] == "failed":
            logger.error(f"Objective failed: {step['step_objective']}")
            return
        logger.info(f"Step #{index + 1} complete: {step['step_objective']}")
        results[step["step_objective"]] = objective_result["result"]
    logger.info("Control creation orchestration complete")


def main(instructions_path: str) -> None:
    with open(instructions_path, "r") as instructions_file:
        orchestration_instructions: OrchestrationInstructions = json.load(instructions_file)
    orchestrate(orchestration_instructions)
