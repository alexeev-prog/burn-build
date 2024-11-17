import subprocess
import shlex
from loguru import logger
from pyburn_build.config.toolchain_config import TargetData
from pyburn_build.config.project_config import ProjectConfig


class BaseBuilder:
	"""
	Base Builder
	"""

	def __init__(
		self, project_config: ProjectConfig, compiler_name: str, target: TargetData
	):
		"""
		Constructs a new instance.

		:param		project_config:	 The project configuration
		:type		project_config:	 ProjectConfig
		:param		compiler_name:	 The compiler name
		:type		compiler_name:	 str
		:param		target:			 The target
		:type		target:			 TargetData
		"""
		self.project_config = project_config
		self.compiler_name = compiler_name
		self.target = target
		self.includes = (
			"-I./".join(self.target.includes) if len(self.target.includes) > 0 else ""
		)
		self.sources = " ".join(self.target.sources)
		self.flags = f"{' '.join(self.project_config.BASE_COMPILER_FLAGS)} {' '.join(self.target.compiler_options)}"
		self.command = f"{self.compiler_name} {self.flags} {self.includes} {self.sources} -o {self.target.output}"

	def execute_commands(self, commands: list):
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
					f'Command "{command}" failed with exit code {result.returncode}: {result.stderr.decode()}'
				)
			else:
				logger.info(f'Successfully run "{command}": {result.stdout.decode()}')

	def run(self):
		"""
		Run builder

		:raises		RuntimeError:  command failed
		"""
		result = subprocess.run(
				shlex.split(self.command), stdout=subprocess.PIPE, stderr=subprocess.PIPE
			)
		if result.returncode != 0:
			raise RuntimeError(
				f'Command "{self.command}" failed with exit code {result.returncode}: {result.stderr.decode()}'
			)
		else:
			logger.info(f'Successfully run "{self.command}": {result.stdout.decode()}')


class CBuilder(BaseBuilder):
	"""
	C Builder
	"""

	def __init__(
		self, project_config: ProjectConfig, compiler_name: str, target: TargetData
	):
		"""
		Constructs a new instance.

		:param		project_config:	 The project configuration
		:type		project_config:	 ProjectConfig
		:param		compiler_name:	 The compiler name
		:type		compiler_name:	 str
		:param		target:			 The target
		:type		target:			 TargetData
		"""
		super(CBuilder, self).__init__(project_config, compiler_name, target)


class CPPBuilder(BaseBuilder):
	"""
	CPP Builder
	"""

	def __init__(
		self, project_config: ProjectConfig, compiler_name: str, target: TargetData
	):
		"""
		Constructs a new instance.

		:param		project_config:	 The project configuration
		:type		project_config:	 ProjectConfig
		:param		compiler_name:	 The compiler name
		:type		compiler_name:	 str
		:param		target:			 The target
		:type		target:			 TargetData
		"""
		super(CPPBuilder, self).__init__(project_config, compiler_name, target)


class CustomBuilder(BaseBuilder):
	"""
	Custom builder
	"""

	def __init__(
		self, project_config: ProjectConfig, compiler_name: str, target: TargetData
	):
		"""
		Constructs a new instance.

		:param		project_config:	 The project configuration
		:type		project_config:	 ProjectConfig
		:param		compiler_name:	 The compiler name
		:type		compiler_name:	 str
		:param		target:			 The target
		:type		target:			 TargetData
		"""
		super(CustomBuilder, self).__init__(project_config, compiler_name, target)
