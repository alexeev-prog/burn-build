import json
from pathlib import Path
from enum import Enum
import yaml
import toml


class ConfigType(Enum):
	"""
	This class has project configuration types.
	"""

	TOML = 0
	YAML = 1
	JSON = 2


class ConfigReader:
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
		self.config_file = Path(config_file)
		self.configtype = configtype
		self.config = self._load_config()

	def _load_data_from_config(self) -> dict:
		"""
		Loads a data from configuration.

		:returns:	configuration dictionary
		:rtype:		dict
		"""
		with open(self.config_file, "r") as fh:
			if self.configtype == ConfigType.YAML:
				data = yaml.load(fh, Loader=yaml.FullLoader)
			elif self.configtype == ConfigType.TOML:
				data = toml.loads(fh)
			elif self.configtype == ConfigType.JSON:
				data = json.load(fh)

		return data
