from rich.traceback import install
from rich import print
import requests

install(show_locals=True)

__version__ = "0.3.4"


def check_for_update():
	try:
		response = requests.get("https://pypi.org/pypi/pyburn_build/json").json()

		latest_version = response["info"]["version"]

		if latest_version != __version__:
			print(f"[bold]New version of library available: {latest_version}[/bold]")
	except requests.RequestException:
		print(f"Version updates information not available. Your version: {__version__}")


check_for_update()
