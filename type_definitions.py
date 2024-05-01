from typing import Optional, TypedDict, Literal

ObjectiveStatus = Literal["completed", "failed"]


class StepInstructions(TypedDict):
    step_objective: str
    step_prompt: str


class StepResult(TypedDict):
    text_output: str
    files_map: dict[str, str]


class ObjectiveResult(StepResult):
    objective_status: ObjectiveStatus


class OrchestrationStaticInstructions(TypedDict):
    main_prompt: str
    step_instructions: list[StepInstructions]


class OrchestrationResearchInstructions(TypedDict):
    research_prompt: str
    research_files: list[str]


class OrchestrationInstructions(OrchestrationResearchInstructions, OrchestrationStaticInstructions):
    control_name: str
    executable_name: Optional[str]
