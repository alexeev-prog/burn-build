import os
import hashlib
import json
from typing import Dict
from rich import print


class BuildCache:
	"""
	This class describes a build cache.
	"""

	def __init__(self, cache_file: str):
		"""
		Constructs a new instance.

		:param		cache_file:	 The cache file
		:type		cache_file:	 str
		"""
		self.cache_file = cache_file
		self.cache_data: Dict[str, str] = self.load_cache()

	def load_cache(self) -> Dict[str, str]:
		"""
		Loads a cache.

		:returns:	cache dict
		:rtype:		Dict[str, str]
		"""
		print(f"[italic dim] Load cache file: {self.cache_file}[/italic dim]")
		if os.path.exists(self.cache_file):
			with open(self.cache_file, "r") as file:
				return json.load(file)

		return {}

	def save_cache(self):
		"""
		Saves a cache.
		"""
		print(f"[italic dim] Save cache file: {self.cache_file}[/italic dim]")
		with open(self.cache_file, "w") as file:
			json.dump(self.cache_data, file, indent=4)

	def get_file_hash(self, file_path: str) -> str:
		"""
		Gets the file hash.

		:param		file_path:	The file path
		:type		file_path:	str

		:returns:	The file hash.
		:rtype:		str
		"""
		hasher = hashlib.sha256()

		with open(file_path, "rb") as file:
			while chunk := file.read(8192):
				hasher.update(chunk)

		return hasher.hexdigest()

	def is_file_uptodate(self, file_path: str) -> bool:
		"""
		Determines whether the specified file path is file uptodate.

		:param		file_path:	The file path
		:type		file_path:	str

		:returns:	True if the specified file path is file uptodate, False otherwise.
		:rtype:		bool
		"""
		current_hash = self.get_file_hash(file_path)
		result = self.cache_data.get(file_path) == current_hash

		return result

	def update_cache(self, file_path: str):
		"""
		Update file cache

		:param		file_path:	The file path
		:type		file_path:	str
		"""
		self.cache_data[file_path] = self.get_file_hash(file_path)
		self.save_cache()
