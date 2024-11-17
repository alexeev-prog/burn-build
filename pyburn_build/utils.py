from pathlib import Path
import re


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
