from pathlib import Path
import re
import os
import subprocess
import shlex
from rich import print


class CommandManager:
	"""
	This class describes an command manager.
	"""

	@staticmethod
	def run_command(command: str) -> int:
		"""
		Run a command in the shell

		:param		command:	   The command
		:type		command:	   str

		:returns:	return code
		:rtype:		int

		:raises		RuntimeError:  command failed
		"""

		print(
			f"[italic] Execute command: [/italic]: [white on black]{command}[/white on black]"
		)

		result = subprocess.run(
			shlex.split(command), stdout=subprocess.PIPE, stderr=subprocess.PIPE
		)

		if result.returncode != 0:
			raise RuntimeError(
				f'Command "{command}" failed with exit code {result.returncode}:\n{result.stderr.decode()}'
			)
		else:
			print(f'[green bold]Successfully run[/green bold] "{command}"'.strip())

		return result.returncode

	@staticmethod
	def change_directory(path: str):
		"""
		Change current directory

		:param		path:  The path
		:type		path:  str
		"""
		os.chdir(path)
		print(f"[bold]Directory changed: {path}[/bold]")


def validate_project_name(project_name: str):
	"""
	Validate project name

	:param		project_name:  The project name
	:type		project_name:  str

	:raises		ValueError:	   invalid project name
	"""
	if not re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*$", project_name):
		raise ValueError(
			"Invalid project name. Must start with a letter or underscore and contain only letters, digits, and underscores."
		)


def create_directory(path: Path):
	"""
	Creates a directory if not exist.

	:param		path:  The path
	:type		path:  Path
	"""
	Path(path).mkdir(parents=True, exist_ok=True)


def execute_commands(commands: list):
	"""
	Execute commands

	:param		commands:	   The commands
	:type		commands:	   list

	:raises		RuntimeError:  command failed
	"""
	for command in commands:
		print(
			f"[italic] Execute command: [/italic]: [white on black]{command}[/white on black]"
		)
		result = subprocess.run(
			shlex.split(command), stdout=subprocess.PIPE, stderr=subprocess.PIPE
		)
		if result.returncode != 0:
			raise RuntimeError(
				f'Command "{command}" failed with exit code {result.returncode}:\n{result.stderr.decode()}'
			)
		else:
			print(
				f'[green bold]Successfully run[/green bold] "{command}":\n{result.stdout.decode()}'
			)
