from pathlib import Path
import re
import subprocess
import shlex
from loguru import logger


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
		logger.info(f"Execute command: {command}")
		result = subprocess.run(
			shlex.split(command), stdout=subprocess.PIPE, stderr=subprocess.PIPE
		)
		if result.returncode != 0:
			raise RuntimeError(
				f'Command "{command}" failed with exit code {result.returncode}:\n{result.stderr.decode()}'
			)
		else:
			logger.info(f'Successfully run "{command}": {result.stdout.decode()}')
