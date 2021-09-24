
from sanic import Blueprint, Request
from changeme.home.forms import LoginForm
from changeme.shortcuts import async_render
from changeme.utils.templates import TemplateData, MenuOption
from changeme.utils import icons
from dataclasses import dataclass

# https://community.sanicframework.org/t/app-url-for-method-view-that-s-not-in-the-same-module-as-app/706/2

bp = Blueprint("home")

bp.static("/static", "public/", name="public")


blog = MenuOption(link="blog/",
                  title="blog",
                  icon_color="text-blue-500",
                  icon_path=icons.book)
about = MenuOption(link="about/", title="about",
                   icon_color="text-yellow-500",
                   icon_path=icons.question)

html_data = TemplateData(
    navbar=[blog, about],
    title="Algorinfo",
    content=dict(msg="hi"),
    meta=dict(test="pepe")

)


@bp.get("/test-form")
async def test_form(request: Request):

    form = LoginForm()

    html_data.content = dict(msg="byes!", form=form)
    # return await async_render(request, "layout.html", data={"msg": "hi"})
    return await async_render(request, "layout.html", html_data)


@bp.get("/")
async def index(request: Request):

    form = LoginForm()

    html_data.content = dict(msg="hi!", form=form)
    # return await async_render(request, "layout.html", data={"msg": "hi"})
    return await async_render(request, "index.html", html_data)
