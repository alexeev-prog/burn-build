from typing import Union
from loguru import logger
from rich import print
from pyburn_build.config.project_config import ProjectConfig
from pyburn_build.config.toolchain_config import ToolchainConfig
from pyburn_build.config.toolchain_config import TargetData
from pyburn_build.builders.builders import (
	CBuilder,
	CPPBuilder,
	CustomBuilder,
	BaseBuilder,
)
from pyburn_build.templates import TEMPLATES
from pyburn_build.utils import execute_commands


def get_builder(
	project_config: ProjectConfig, compiler_name: str, target: TargetData
) -> BaseBuilder:
	"""
	Gets the builder.

	:param		project_config:	 The project configuration
	:type		project_config:	 ProjectConfig
	:param		compiler_name:	 The compiler name
	:type		compiler_name:	 str
	:param		target:			 The target
	:type		target:			 TargetData

	:returns:	The builder.
	:rtype:		BaseBuilder
	"""
	compiler_name = compiler_name.lower()

	if compiler_name == "gcc" or compiler_name == "clang":
		return CBuilder(project_config, compiler_name, target)
	elif compiler_name == "g++" or compiler_name == "clang++":
		return CPPBuilder(project_config, compiler_name, target)
	else:
		return CustomBuilder(project_config, compiler_name, target)


class BuildManager:
	"""
	This class describes a build manager.
	"""

	def __init__(
		self, project_config: ProjectConfig, toolchain_config: ToolchainConfig
	):
		"""
		Constructs a new instance.

		:param		project_config:	   The project configuration
		:type		project_config:	   ProjectConfig
		:param		toolchain_config:  The toolchain configuration
		:type		toolchain_config:  ToolchainConfig
		"""
		self.project_config = project_config
		self.toolchain_config = toolchain_config

		self.default_compiler = self.project_config.COMPILER_NAME
		self.language = self.project_config.LANGUAGE

		self.supported_compilers = ["gcc", "g++", "clang", "clang++"]

	def build(self, targets: Union[list, str]):
		"""
		Build project

		:param		targets:  The targets
		:type		targets:  Union[list, str]
		"""
		logger.info(f'{"=" * 16} Start build (targets: {targets})')

		print(
			f'[cyan]{"=" * 4} Execute prelude commands: {self.toolchain_config.prelude_commands}[/cyan]'
		)

		execute_commands(self.toolchain_config.prelude_commands)

		for target in self.toolchain_config.targets:
			if targets == "all" or target in targets:
				logger.debug(f'{"=" * 8} Start Build Target {target.name}')
				print(f'[cyan]{"=" * 8} Start Build Target {target.name}[/cyan]')

				compiler = (
					target.compiler
					if target.compiler is not None
					else self.default_compiler
				)

				if compiler.lower() not in self.supported_compilers:
					logger.warn("Compiler not supported, using CustomBuilder...")

				builder = get_builder(self.project_config, compiler, target)

				print(f'[blue bold]{"=" * 8} RUN BUILD [/blue bold]')

				if self.project_config.USE_CMAKE:
					print("[blue] Use CMake Builder[/blue]")
					print("[yellow bold]Support only C++ projects[/yellow bold]")

					with open("cmake_build.sh", "w") as file:
						file.write(TEMPLATES["build.sh"])

					execute_commands(
						[
							"bash cmake_build.sh",
						]
					)
				else:
					print("[blue] Use Built-in Builder[/blue]")
					builder.run()

				print(f'[cyan]{"=" * 8} End Build Target {target.name}[/cyan]')
				logger.debug(f'{"=" * 8} End Build Target {target.name}')
			else:
				logger.debug(f"Skip target: {target.name}")

		print(
			f'[cyan]{"=" * 4} Execute post commands: {self.toolchain_config.post_commands}[/cyan]'
		)
		execute_commands(self.toolchain_config.post_commands)
