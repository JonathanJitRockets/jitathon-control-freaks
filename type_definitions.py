from typing import TypedDict, Literal

ObjectiveStatus = Literal["completed", "failed"]


class StepInstructions(TypedDict):
    step_objective: str
    step_prompt: str


class StepResult(TypedDict):
    text_output: str
    files_map: dict[str, str]


class ObjectiveResult(TypedDict):
    objective_status: ObjectiveStatus
    result: StepResult


class OrchestrationInstructions(TypedDict):
    main_prompt: str
    step_instructions: list[StepInstructions]
