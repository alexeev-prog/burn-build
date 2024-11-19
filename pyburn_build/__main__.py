import click
from rich.console import Console
from rich.prompt import Prompt, Confirm
from pyburn_build.config.base import ConfigType
from pyburn_build.config.project_config import ProjectConfigReader
from pyburn_build.config.toolchain_config import ToolchainConfigReader
from pyburn_build.creator import ProjectArchitecture
from pyburn_build.builders.build_manager import BuildManager
from pyburn_build.utils import CommandManager
from pyburn_build.config.configsaver import write_file
from pyburn_build.exceptions import UnknownTargetError

console = Console()


def config_type_by_file(filename: str) -> ConfigType:
	"""
	Get config type by file

	:param		filename:  The filename
	:type		filename:  str

	:returns:	The configuration type.
	:rtype:		ConfigType
	"""
	if filename.split(".")[-1] == "json":
		return ConfigType.JSON
	elif filename.split(".")[-1] == "yaml":
		return ConfigType.YAML
	elif filename.split(".")[-1] == "toml":
		return ConfigType.TOML


@click.group()
def cli():
	"""
	Software for quickly creating and building C/C++ projects
	"""
	pass


@cli.command()
@click.option(
	"--output-type", default="json", help="Configuration output type", required=True
)
@click.option(
	"--output-file", default="project_config", help="Output filename", required=True
)
def add_project_config(output_type: str, output_file: str):
	"""
	Adds a project configuration.

	:param		output_type:  The output type
	:type		output_type:  str
	:param		output_file:  The output file
	:type		output_file:  str
	"""
	name = Prompt.ask("Project name")
	version = Prompt.ask("Project Version", default="0.1.0")
	description = Prompt.ask("Description", default="")
	language = Prompt.ask("Language", default="DEFAULT").lower()
	compiler_name = Prompt.ask("Default compiler name")
	base_compiler_flags = Prompt.ask("Base compiler flags", default="").split(" ")
	use_cmake = Confirm.ask("Use CMake", default=False)
	cache_file = Prompt.ask("Cache file (.json)", default="cache_data.json")

	config = {
		"metadata": {
			"name": name,
			"version": version,
			"description": description,
			"language": language,
			"use_cmake": use_cmake,
			"cache_file": cache_file,
		},
		"compiler": {"name": compiler_name, "base_compiler_flags": base_compiler_flags},
	}

	write_file(config, output_file, output_type)


@cli.command()
@click.option("--project-config", help="Path to project config", required=True)
@click.option("--toolchain-config", help="Path to toolchain config", required=True)
def create(project_config: str, toolchain_config: str):
	"""
	Create new project

	:param		interactive:	   The interactive
	:type		interactive:	   bool
	:param		project_config:	   The project configuration
	:type		project_config:	   str
	:param		toolchain_config:  The toolchain configuration
	:type		toolchain_config:  str
	"""
	project_config_type = config_type_by_file(project_config)
	toolchain_config_type = config_type_by_file(toolchain_config)

	pc = ProjectConfigReader(project_config, project_config_type)
	tc = ToolchainConfigReader(toolchain_config, toolchain_config_type)

	console.print(
		f'[green]Load project configuration "{project_config}" successfully.[/green]'
	)
	console.print(
		f'[green]Load toolchain configuration "{toolchain_config}" successfully[/green]'
	)

	pa = ProjectArchitecture(pc.config, tc.config)
	pa.add_file(project_config)
	pa.add_file(toolchain_config)
	pa.run()


@cli.command()
@click.option(
	"--targets", help="Targets for build (default: all)", required=True, default="all"
)
@click.option("--project-config", help="Path to project config", required=True)
@click.option("--toolchain-config", help="Path to toolchain config", required=True)
def build(targets: str, project_config: str, toolchain_config: str):
	"""
	Build project

	:param		project_config:	   The project configuration
	:type		project_config:	   str
	:param		toolchain_config:  The toolchain configuration
	:type		toolchain_config:  str
	"""
	project_config_type = config_type_by_file(project_config)
	toolchain_config_type = config_type_by_file(toolchain_config)

	pc = ProjectConfigReader(project_config, project_config_type)
	tc = ToolchainConfigReader(toolchain_config, toolchain_config_type)

	bm = BuildManager(pc.config, tc.config)

	targets = "all" if targets == "all" else targets.split(",")

	bm.build(targets)


@cli.command()
@click.option("--toolchain-config", help="Path to toolchain config", required=True)
@click.option("--target", help="Target name", required=True)
def run(toolchain_config: str, target: str):
	"""
	Run builded target

	:param		project_config:	   The project configuration
	:type		project_config:	   str
	:param		toolchain_config:  The toolchain configuration
	:type		toolchain_config:  str

	:raises		ValueError:		   Unknown target
	"""
	toolchain_config_type = config_type_by_file(toolchain_config)

	tc = ToolchainConfigReader(toolchain_config, toolchain_config_type)

	for t in tc.config.targets:
		if t.name == target:
			target = t
			break

	if isinstance(target, str):
		raise UnknownTargetError(f"Unknown target: {target}")

	CommandManager.run_command(f"./{target.output}")


def main():
	cli()


if __name__ == "__main__":
	main()
