from rich import print
from pyburn_build.config.toolchain_config import TargetData
from pyburn_build.utils import CommandManager
from pyburn_build.config.project_config import ProjectConfig
from pyburn_build.cache import BuildCache
from pyburn_build.exceptions import SourcesIsUptodate


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
		self.cache = BuildCache(self.project_config.CACHE_FILE)
		self.compiler_name = compiler_name
		self.target = target
		self.includes = (
			"-I" + "".join(self.target.includes)
			if len(self.target.includes) > 0
			else ""
		)
		self.flags = f"{' '.join(self.project_config.BASE_COMPILER_FLAGS)} {' '.join(self.target.compiler_options)}"

		self.sources = " ".join(
			[
				"" if self.cache.is_file_uptodate(source) else source
				for source in self.target.sources
			]
		)

		self.sources = []

		for source in self.target.sources:
			if self.cache.is_file_uptodate(source):
				print(
					f"[yellow]Source {source} finded in cache (skip building)[/yellow]"
				)
				continue
			else:
				self.sources.append(source)
				self.cache.update_cache(source)

		self.sources = " ".join(self.sources) if len(self.sources) > 0 else None

		if self.sources is None:
			raise SourcesIsUptodate("Error: no sources ready for build")

		self.command = f"{self.compiler_name} {self.flags} {self.includes} {self.sources} -o {self.target.output}".strip()

	def run(self):
		"""
		Run builder

		:raises		RuntimeError:  command failed
		"""
		CommandManager.run_command(self.command)
		print()


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
