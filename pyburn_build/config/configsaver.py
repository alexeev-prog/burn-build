import yaml
import toml
import json


def write_file(data: dict, filename: str, filetype: str):
	"""
	Writes a file.

	:param		data:	   The data
	:type		data:	   dict
	:param		filename:  The filename
	:type		filename:  str
	:param		filetype:  The filetype
	:type		filetype:  str
	"""
	with open(filename, "w") as file:
		if filetype == "toml":
			file.write(toml.dumps(data))
		elif filetype == "yaml":
			file.write(yaml.dump(data))
		elif filetype == "json":
			json.dump(data, file, indent=4)
		else:
			file.write(data)
