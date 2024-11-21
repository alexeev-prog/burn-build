MAIN_APP_TEMPLATE = """
import os
from pyechonext.utils.exceptions import MethodNotAllow
from pyechonext.app import ApplicationType, EchoNext
from pyechonext.urls import URL
from pyechonext.config import Settings
from pyechonext.template_engine.builtin import render_template
from pyechonext.middleware import middlewares

from views import IndexView


url_patterns = [URL(url="/", view=IndexView)]
settings = Settings(
	BASE_DIR=os.path.dirname(os.path.abspath(__file__)), TEMPLATES_DIR="templates"
)
echonext = EchoNext(
	{{APPNAME}}, settings, middlewares, urls=url_patterns, application_type=ApplicationType.HTML
)
"""

INDEX_VIEW_TEMPLATE = """
from pyechonext.views import View


class IndexView(View):
	def get(self, request, response, **kwargs):
		return 'Hello World!'

	def post(self, request, response, **kwargs):
		raise MethodNotAllow(f'Request {request.path}: method not allow')
"""

DIRS = {
	"templates": {"index.html": "<h1>Hello World</h1>"},
	"views": {
		"__init__.py": "from views.main import IndexView\nall=(IndexView)",
		"main.py": INDEX_VIEW_TEMPLATE,
	},
}
