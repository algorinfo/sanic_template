# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
from typing import Any, Dict, List
from dataclasses import dataclass
from typing import Callable

from jinja2 import Environment, PackageLoader, Template, select_autoescape
from sanic import Sanic


@dataclass
class MenuOption:
    link: str
    title: str
    icon_path: str
    icon_color: str


@dataclass
class TemplateData:
    navbar: List[MenuOption]
    title: str
    content: Dict[str, Any]
    meta: Dict[str, str]


class Render:
    # inspired by https://community.sanicframework.org/t/using-jinja2-with-sanic/615
    # also see
    # https://github.com/dldevinc/jinja2-simple-tags

    def __init__(self, package_name: str,
                 folder_name: str = "templates/",
                 enable_async=True,
                 encoding="UTF-8"
                 ):
        """
        Example:
        ``` loader = PackageLoader("project.ui", "pages")```
        :param package_name: Import name of the package that contains the template directory.
        :param folder_name: Folder inside of the package which contains the templates
        """
        self._package = package_name
        self._folder = folder_name
        self.encoding = encoding
        self._loader = None
        self.env: Environment = Environment()
        self.build_env(enable_async=enable_async)

    def build_env(self, enable_async=True):
        self._loader = PackageLoader(
            package_name=self._package,
            package_path=self._folder,
            encoding=self.encoding
        )

        self.env: Environment = Environment(
            loader=self._loader,
            autoescape=select_autoescape(),
            enable_async=enable_async
        )

        return self.env

    def add_func(self, name: str, func: Callable):
        self.env.globals[name] = func

    def init_app(self, app: Sanic):
        app.ctx.render = self
        self.env.globals.update(url_for=app.url_for)

    async def async_render(self, request, tpl_name, **kwargs):
        template = self.env.get_template(tpl_name)
        ctx = {
            'request': request.ctx.__dict__,
        }
        rendered = await template.render_async(ctx, **kwargs)
        return rendered

    def get_template(self, tpl_name) -> Template:
        return self.env.get_template(tpl_name)
