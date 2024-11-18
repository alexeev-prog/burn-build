from typing import List
from dataclasses import dataclass, field
from pyburn_build.config.base import ConfigReader, ConfigType


@dataclass
class TargetData:
	"""
	This class describes a target data.
	"""

	name: str
	output: str
	includes: list = field(default_factory=list)
	sources: list = field(default_factory=list)
	compiler: str = None
	compiler_options: list = field(default_factory=list)


@dataclass
class ToolchainConfig:
	"""
	This class describes a toolchain configuration.
	"""

	prelude_commands: List[str] = field(default_factory=list)
	targets: List[TargetData] = field(default_factory=list)
	post_commands: List[str] = field(default_factory=list)


class ToolchainConfigReader(ConfigReader):
	"""
	This class describes a toolchain configuration reader.
	"""

	def __init__(self, config_file: str, configtype: ConfigType = ConfigType.TOML):
		"""
		Constructs a new instance.

		:param		config_file:  The configuration file
		:type		config_file:  str
		:param		configtype:	  The configtype
		:type		configtype:	  ConfigType
		"""
		super(ToolchainConfigReader, self).__init__(config_file, configtype)

	def _load_config(self):
		"""
		Loads a configuration.
		"""
		data = self._load_data_from_config()

		prelude_commands = data.get("prelude_commands", [])
		post_commands = data.get("post_commands", [])

		targets = data.get("targets", {})
		data_targets = []

		for target_name, target in targets.items():
			if target_name == "all":
				raise ValueError("Target name is forbidden: all")

			data_targets.append(
				TargetData(
					name=target_name,
					output=target.get("output", "bin/a.out"),
					compiler_options=target.get("compiler_options", []),
					sources=target.get("sources", []),
					includes=target.get("includes", []),
					compiler=target.get("compiler", None),
				)
			)

		config = ToolchainConfig(
			prelude_commands=prelude_commands,
			targets=data_targets,
			post_commands=post_commands,
		)

		return config
