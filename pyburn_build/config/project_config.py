from dataclasses import dataclass, field
from pyburn_build.config.base import ConfigReader, ConfigType
from pyburn_build.exceptions import ProjectConfigError


@dataclass
class ProjectConfig:
	"""
	This class describes a project configuration.
	"""

	NAME: str
	VERSION: str
	DESCRIPTION: str
	LANGUAGE: str = "DEFAULT"
	CACHE_FILE: str = "build_cache.json"

	COMPILER_NAME: str = None
	BASE_COMPILER_FLAGS: list = field(default_factory=list)

	USE_CMAKE: bool = False

	EXTRA: dict = field(default_factory=dict)


class ProjectConfigReader(ConfigReader):
	"""
	This class describes a project configuration reader.
	"""

	def __init__(self, config_file: str, configtype: ConfigType = ConfigType.TOML):
		"""
		Constructs a new instance.

		:param		config_file:  The configuration file
		:type		config_file:  str
		:param		configtype:	  The configtype
		:type		configtype:	  ConfigType
		"""
		super(ProjectConfigReader, self).__init__(config_file, configtype)

	def _load_config(self) -> ProjectConfig:
		"""
		Loads a configuration.

		:returns:	The project configuration.
		:rtype:		ProjectConfig

		:raises		ValueError:	 config dont include metadata/compiler
		"""
		data = self._load_data_from_config()
		metadata = data.get("metadata", None)
		compiler = data.get("compiler", None)

		if metadata is None:
			raise ProjectConfigError(
				"The project configuration must include metadata (name, version, description, language)"
			)
		elif compiler is None:
			raise ProjectConfigError(
				"The project configuration must include compiler (name, base_compiler_flags, linker_flags)"
			)

		config = ProjectConfig(
			NAME=metadata.get("name", "myApp"),
			VERSION=metadata.get("version", "0.1.0"),
			DESCRIPTION=metadata.get("description", "my application"),
			LANGUAGE=metadata.get("language", "DEFAULT"),
			USE_CMAKE=metadata.get("use_cmake", False),
			COMPILER_NAME=compiler.get("name", None),
			BASE_COMPILER_FLAGS=compiler.get("base_compiler_flags", []),
			CACHE_FILE=metadata.get("cache_file", "build_cache.json"),
		)

		return config
