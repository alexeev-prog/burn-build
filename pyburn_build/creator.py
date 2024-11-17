import os
from pathlib import Path
from loguru import logger
from pyburn_build.config.project_config import ProjectConfig
from pyburn_build.config.toolchain_config import ToolchainConfig
from pyburn_build.templates import TEMPLATES
from pyburn_build.utils import create_directory


class ProjectArchitecture:
	"""
	This class describes a project architecture.
	"""

	def __init__(
		self, project_config: ProjectConfig, toolchain_config: ToolchainConfig
	):
		"""
		Constructs a new instance.

		:param		project_config:	 The project configuration
		:type		project_config:	 ProjectConfig
		"""
		self.project_config = project_config
		self.toolchain_config = toolchain_config

		self.base_dir = Path(self.project_config.NAME)
		self.docs_dir = self.base_dir / "docs"

		self.extra_dirs = []
		self.files = []

		self.added_files = []

		if self.project_config.LANGUAGE.lower() == "python":
			self.files += [
				"pyproject.toml",
			]
			self.extra_dirs += [
				self.base_dir / "src",
			]
		elif (
			self.project_config.LANGUAGE.lower() == "cpp"
			or self.project_config.LANGUAGE.lower() == "c++"
		):
			self.files += ["CMakeLists.txt", ".clang-format"]
			self.extra_dirs += [self.base_dir / "src", self.base_dir / "include"]

		for target in self.toolchain_config.targets:
			self._iteraite_files(target.includes)
			self._iteraite_files(target.sources)
			self._iteraite_files(
				[
					target.output,
				]
			)

	def _iteraite_files(self, files: list):
		"""
		Iteraite files

		:param		files:	The files
		:type		files:	list
		"""
		for file in files:
			file = os.path.join(self.base_dir, file)
			directory = os.path.dirname(file)
			os.makedirs(directory, exist_ok=True)

			if not os.path.exists(file):
				with open(file, "a") as f:
					f.write(f"{file}")

	def add_file(self, filename: str):
		"""
		Adds a file.

		:param		filename:  The filename
		:type		filename:  str
		"""
		self.added_files.append(filename)

	def _create_files(self):
		"""
		Creates files.
		"""
		for file in self.files:
			logger.debug(f"Create file: {file}")
			with open(os.path.join(self.base_dir, file), "w") as f:
				f.write(TEMPLATES.get(file, file))

		for file in self.added_files:
			logger.debug(f"Create file: {file}")
			with open(file, "r") as src:
				file = file.split("/")[-1]
				with open(os.path.join(self.base_dir, file), "w") as dist:
					dist.write(src.read())

	def _create_dirs(self):
		"""
		Creates dirs.
		"""
		logger.debug(f"Create directory: {self.base_dir}")
		create_directory(self.base_dir)
		logger.debug(f"Create directory: {self.docs_dir}")
		create_directory(self.docs_dir)

		for extra_dir in self.extra_dirs:
			logger.debug(f"Create directory: {extra_dir}")
			create_directory(extra_dir)

	def run(self):
		"""
		Run project creation
		"""
		logger.info("Project creation runned...")

		self._create_dirs()

		self._create_files()

		logger.info("Project created successfully!")
