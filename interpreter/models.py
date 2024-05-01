import os
import subprocess
from abc import abstractmethod
from typing import Union

from pydantic import BaseModel


class TaskInputRunner(BaseModel):
    def run(self, working_dir) -> str:
        """
        Print the current working directory and call the subclass-specific implementation of the task.
        """
        # directory_info = f"Current directory: {os.getcwd()}\n"
        # The subclass implementation of _run needs to be defined in each subclass
        child_run_res = self._run(working_dir=working_dir)
        return child_run_res + '\nYour current directory is:' + working_dir

    @abstractmethod
    def _run(self, working_dir) -> str:
        """
        This is the actual method to be implemented by subclasses for specific tasks.
        """
        raise NotImplementedError("Subclasses must implement this method")


class WriteFileTaskInput(TaskInputRunner):
    file_name: str
    file_content: str

    def _run(self, working_dir) -> str:
        """
        Attempts to write content to a specified file and returns 'Done' on success.
        If the write operation fails, it returns only the specific error message related to the file write failure.
        """
        try:
            path = working_dir + '/' + self.file_name
            with open(path, 'w') as file:
                file.write(self.file_content)
            if os.path.exists(path):
                return "Done"
            else:
                return "Error: File does not exist after writing."
        except Exception as e:
            return str(e)


class CommandTaskInput(TaskInputRunner):
    command: str

    def _run(self, working_dir) -> str:
        """
        Executes the specified command using the system shell and returns the output.
        If the command fails, it returns the error generated by the command.
        """
        try:
            result = subprocess.run(self.command, shell=True, check=True, text=True, stdout=subprocess.PIPE,
                                    cwd=working_dir,
                                    stderr=subprocess.PIPE)
            return result.stdout or result.stderr or "Done"
        except subprocess.CalledProcessError as e:
            return e.stderr


class ReadFileTaskInput(TaskInputRunner):
    file_name: str

    def _run(self, working_dir) -> str:
        """
        Attempts to read the content of a file specified by file_name and returns the content.
        If the read operation fails, it returns the error message from the exception directly.
        """
        try:
            with open(working_dir + '/' + self.file_name, 'r') as file:
                content = file.read()
            return content
        except Exception as e:
            return str(e)


TaskInput = Union[WriteFileTaskInput, CommandTaskInput, ReadFileTaskInput]
