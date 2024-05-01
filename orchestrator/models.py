from abc import abstractmethod
from typing import Union

from pydantic import BaseModel


class TaskInputRunner(BaseModel):
    @abstractmethod
    def run(self):
        pass


class WriteFileTaskInput(TaskInputRunner):
    file_name: str
    file_content: str

    def run(self):
        pass


class CommandTaskInput(TaskInputRunner):
    command: str

    def run(self):
        pass


class ReadFileTaskInput(TaskInputRunner):
    file_name: str

    def run(self):
        pass


TaskInput = Union[WriteFileTaskInput, CommandTaskInput, ReadFileTaskInput]


class Task(BaseModel):
    current_objective: str
    required_task: str
    task_input: TaskInput
