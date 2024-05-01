import unittest
import os
import subprocess

from orchestrator.models import WriteFileTaskInput, CommandTaskInput, ReadFileTaskInput


# Assuming the classes WriteFileTaskInput, CommandTaskInput, and ReadFileTaskInput are already defined.

class TestTaskInputRunners(unittest.TestCase):

    def test_write_file_task_input_success(self):
        """ Test writing to a file successfully. """
        task_input = WriteFileTaskInput(file_name="testfile.txt", file_content="Hello, world!")
        result = task_input.run()
        self.assertEqual(result, "Done")
        # Clean up
        os.remove("testfile.txt")

    def test_write_file_task_input_failure(self):
        """ Test handling of file write failures (e.g., permission issues). """
        task_input = WriteFileTaskInput(file_name="/unwritable/testfile.txt", file_content="Hello, world!")
        result = task_input.run()
        self.assertTrue("Err" in result)

    def test_command_task_input_success(self):
        """ Test executing a command successfully. """
        task_input = CommandTaskInput(command="echo Hello")
        result = task_input.run()
        self.assertEqual(result.strip(), "Hello")

    def test_command_task_input_failure(self):
        """ Test handling of command execution failures. """
        task_input = CommandTaskInput(command="exit 1")
        result = task_input.run()
        self.assertTrue(result.strip() == "")

    def test_read_file_task_input_success(self):
        """ Test reading from a file successfully. """
        with open("testfile.txt", "w") as f:
            f.write("Hello, world!")
        task_input = ReadFileTaskInput(file_name="testfile.txt")
        result = task_input.run()
        self.assertEqual(result, "Hello, world!")
        # Clean up
        os.remove("testfile.txt")

    def test_read_file_task_input_failure(self):
        """ Test handling of file read failures (e.g., file not found). """
        task_input = ReadFileTaskInput(file_name="nonexistentfile.txt")
        result = task_input.run()
        self.assertTrue("No such file or directory" in result)

