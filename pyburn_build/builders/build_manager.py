from typing import Union
from multiprocessing import Process, Pool, cpu_count
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
from pyburn_build.utils import (
	CommandManager,
	print_header,
	print_step,
	print_substep,
	print_message,
)
from pyburn_build.exceptions import SourcesIsUptodate


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

	def _build_target(self, target):
		print_header(f"TARGET {target.name}", f"Start Build Target: {target.name}")

		compiler = (
			target.compiler if target.compiler is not None else self.default_compiler
		)

		if compiler.lower() not in self.supported_compilers:
			print_message(
				f"TARGET {target.name}",
				"[yellow bold]Compiler not supported, using CustomBuilder...[/yellow bold]",
			)

		try:
			builder = get_builder(self.project_config, compiler, target)
		except SourcesIsUptodate as ex:
			print_message(
				f"TARGET {target.name}",
				f"[yellow bold]Skip target {target.name}: all sources is up to date ({ex})[/yellow bold]\n",
			)
			return

		print_step(f"BUILD TARGET {target.name}", f"RUN BUILD {target.name}")

		if self.project_config.USE_CMAKE:
			print_substep("note", "[blue] Use CMake Builder[/blue]")
			print_message(
				"warning", "[yellow bold]Support only C++ projects[/yellow bold]"
			)

			with open("cmake_build.sh", "w") as file:
				file.write(TEMPLATES["build.sh"])

			p = Process(
				target=CommandManager.run_command, args=("bash cmake_build.sh",)
			)
			p.start()
			p.join()
		else:
			print_substep(f"TARGET {target.name}", "[blue] Use Built-in Builder[/blue]")

			builder.run()

		print_step(f"TARGET {target.name} END BUILD", f"END BUILD {target.name}")

	def _run_build_process(self, targets: Union[list, str]):
		if targets == "all":
			print_message(
				"debug",
				f"Create pool with processes: {cpu_count()} (for run build process). Targets: {targets}",
			)
			with Pool(processes=cpu_count()) as pool:
				targets = self.toolchain_config.targets
				pool.map(self._build_target, targets)
		else:
			_targets = []
			for t in self.toolchain_config.targets:
				if t in targets:
					self._targets.append(t)
				else:
					print_message(
						f"TARGET {t.name}", f"[bold]Skip target: {t.name}[/bold]\n"
					)

			print_message(
				"debug",
				f"Create pool with processes: {cpu_count()} (for run build process). Targets: {targets}",
			)
			with Pool(processes=cpu_count()) as pool:
				targets = _targets
				pool.map(self._build_target, targets)

	def build(self, targets: Union[list, str]):
		"""
		Build project

		:param		targets:  The targets
		:type		targets:  Union[list, str]
		"""
		print_header(
			"TARGETS BUILD", f"[green]Start build (targets: {targets})[/green]"
		)

		print_step(
			"TOOLCHAIN",
			f"Execute prelude commands: {self.toolchain_config.prelude_commands}",
		)

		print_message(
			"debug",
			f"Create pool with processes: {cpu_count()} (for run prelude commands)",
		)
		with Pool(processes=cpu_count()) as pool:
			pool.map(CommandManager.run_command, self.toolchain_config.prelude_commands)

		print()

		# process = Process(target=self._run_build_process, args=(targets,))
		# process.start()
		# process.join()
		print_step("RUN BUILD PROCESS", f"Run build process for targets: {targets}")
		self._run_build_process(targets)

		print_step(
			"TOOLCHAIN", f"Execute post commands: {self.toolchain_config.post_commands}"
		)

		print_message(
			"debug",
			f"Create pool with processes: {cpu_count()} (for run post commands)",
		)
		with Pool(processes=cpu_count()) as pool:
			pool.map(CommandManager.run_command, self.toolchain_config.post_commands)
