from typing import TypedDict, Literal

from pydantic import BaseModel

from interpreter.models import TaskInput

ObjectiveStatus = Literal["completed", "failed"]


class StepInstructions(TypedDict):
    step_objective: str
    step_prompt: str


class StepResult(TypedDict):
    text_output: str
    files_map: dict[str, str]


class StepOutput(BaseModel):
    current_objective: str
    required_task: str
    task_input: TaskInput


class ObjectiveResult(StepResult):
    objective_status: ObjectiveStatus


class OrchestrationStaticInstructions(TypedDict):
    main_prompt: str
    step_instructions: list[StepInstructions]


class OrchestrationResearchInstructions(TypedDict):
    research_prompt: str
    research_files: list[str]


class OrchestrationInstructions(OrchestrationStaticInstructions, OrchestrationResearchInstructions):
    pass
