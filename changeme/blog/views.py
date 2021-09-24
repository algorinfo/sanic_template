from sanic import Blueprint, Request, json
from sanic.views import HTTPMethodView
from changeme.blog.api import ArticleApi
from changeme.utils import icons
from changeme.shortcuts import async_render
from changeme.utils.templates import MenuOption, TemplateData

article_api = ArticleApi()

_LIMIT = 10

bp = Blueprint("blog", url_prefix="/blog")


blog = MenuOption(link="/blog",
                  title="blog",
                  icon_color="text-blue-500",
                  icon_path=icons.book)
about = MenuOption(link="/about", title="about",
                   icon_color="text-yellow-500",
                   icon_path=icons.question)

html_data = TemplateData(
    navbar=[blog, about],
    title="Algorinfo",
    content=dict(msg="hi"),
    meta=dict(test="pepe")

)


class BlogView(HTTPMethodView):
    async def get(self, request):

        session = request.ctx.session
        async with session.begin():
            response = await article_api.get_all(
                session, 1, _LIMIT)

        html_data.content = response.rows

        return await async_render(request, "blog/index.html", html_data)


class EditorView(HTTPMethodView):
    async def get(self, request):
        # html_data.content = response.rows
        return await async_render(request, "blog/editor2.html", html_data)

    

bp.add_route(BlogView.as_view(), "/")
bp.add_route(EditorView.as_view(), "/editor")
