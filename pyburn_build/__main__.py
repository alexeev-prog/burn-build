import click
from rich.console import Console
from loguru import logger
from pyburn_build.config.base import ConfigType
from pyburn_build.config.project_config import ProjectConfigReader
from pyburn_build.config.toolchain_config import ToolchainConfigReader
from pyburn_build.creator import ProjectArchitecture
from pyburn_build.builders.build_manager import BuildManager

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
	Software for quickly creating C++ projects
	"""
	pass


@cli.command()
@click.option("--interactive", is_flag=True, help="Run an interactive mode")
@click.option("--project-config", help="Path to project config", required=True)
@click.option("--toolchain-config", help="Path to toolchain config", required=True)
def create(interactive: bool, project_config: str, toolchain_config: str):
	"""
	Create project

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

	logger.info(f'Load project configuration "{project_config}" successfully.')
	logger.info(f'Load toolchain configuration "{toolchain_config}" successfully')

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

	targets = 'all' if targets == 'all' else targets.split(',')

	bm.build(targets)


@cli.command()
@click.argument("project_config")
def show_project_config(project_config: str):
	"""
	Shows the project configuration.

	:param		project_config:	 The project configuration
	:type		project_config:	 str
	"""
	project_config_type = config_type_by_file(project_config)
	pc = ProjectConfigReader(project_config, project_config_type)

	console.print(f'{"=" * 30} Metadata {"=" * 30}')
	console.print(f"Project Name: {pc.config.NAME}")
	console.print(f"Project Version: {pc.config.VERSION}")
	console.print(f"Project Main Language: {pc.config.LANGUAGE}")
	console.print(f'{"=" * 30} Compiler {"=" * 30}')
	console.print(f"Compiler Name: {pc.config.COMPILER_NAME}")
	console.print(f"Base Compiler Flags: {pc.config.BASE_COMPILER_FLAGS}")
	console.print(f"Compiler Linker Flags: {pc.config.COMPILER_LINKER_FLAGS}")
	console.print(f"\nExtra: {pc.config.EXTRA}")


@cli.command()
@click.argument("toolchain_config")
def show_toolchain_config(toolchain_config: str):
	"""
	Shows the toolchain configuration.

	:param		toolchain_config:  The toolchain configuration
	:type		toolchain_config:  str
	"""
	toolchain_config_type = config_type_by_file(toolchain_config)
	tc = ToolchainConfigReader(toolchain_config, toolchain_config_type)

	console.print(f"Prelude Commands: {tc.config.prelude_commands}")
	console.print(f"Post commands: {tc.config.post_commands}")

	for target in tc.config.targets:
		console.print(f'{"=" * 30} Target {target.name} {"=" * 30}')
		console.print(f"Sources: {target.sources}")
		console.print(f"Includes: {target.includes}")
		console.print(f"Dependencies: {target.dependencies}")
		console.print(f"Output: {target.output}")
		console.print(f"Compiler options: {target.compiler_options}")


@cli.command()
@click.option("--project-config", help="Path to project config", required=True)
@click.option("--toolchain-config", help="Path to toolchain config", required=True)
def show_configs(project_config: str, toolchain_config: str):
	project_config_type = config_type_by_file(project_config)
	pc = ProjectConfigReader(project_config, project_config_type)

	console.print(f'{"=" * 50} PROJECT {"=" * 50}')

	console.print(f'{"=" * 30} Metadata {"=" * 30}')
	console.print(f"Project Name: {pc.config.NAME}")
	console.print(f"Project Version: {pc.config.VERSION}")
	console.print(f"Project Main Language: {pc.config.LANGUAGE}")
	console.print(f'{"=" * 30} Compiler {"=" * 30}')
	console.print(f"Compiler Name: {pc.config.COMPILER_NAME}")
	console.print(f"Base Compiler Flags: {pc.config.BASE_COMPILER_FLAGS}")
	console.print(f"Compiler Linker Flags: {pc.config.COMPILER_LINKER_FLAGS}")
	console.print(f"\nExtra: {pc.config.EXTRA}")

	toolchain_config_type = config_type_by_file(toolchain_config)
	tc = ToolchainConfigReader(toolchain_config, toolchain_config_type)

	console.print(f'{"=" * 50} TOOLCHAIN {"=" * 50}')

	console.print(f"Prelude Commands: {tc.config.prelude_commands}")
	console.print(f"Post commands: {tc.config.post_commands}")

	for target in tc.config.targets:
		console.print(f'{"=" * 30} Target {target.name} {"=" * 30}')
		console.print(f"Sources: {target.sources}")
		console.print(f"Includes: {target.includes}")
		console.print(f"Dependencies: {target.dependencies}")
		console.print(f"Output: {target.output}")
		console.print(f"Compiler options: {target.compiler_options}")


def main():
	cli()


if __name__ == "__main__":
	main()
