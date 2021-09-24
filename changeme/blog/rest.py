from datetime import datetime
from typing import List, Optional

from sanic import Blueprint, Request, json
from sanic_openapi import doc
from changeme.blog.api import ArticleApi, CategoryApi
from changeme.blog.serializers import (ArticlePost, CategoryPost,
                                      CategoryResponse)

bp = Blueprint("blogapi", url_prefix="/blog", version="v1")

article_api = ArticleApi()
category_api = CategoryApi()


def _parse_page_limit(request, def_pg="1", def_lt="100"):
    strpage = request.args.get("page", [def_pg])
    strlimit = request.args.get("limit", [def_lt])
    page = int(strpage[0])
    limit = int(strlimit[0])

    return page, limit


@bp.get("/article/category/<category_id:int>")
@doc.consumes(doc.Integer(name="category_id"), location="path")
@doc.tag("article")
async def get_articles_category(request: Request, category_id: int):

    page, limit = _parse_page_limit(request)

    session = request.ctx.session
    async with session.begin():
        response = await article_api.by_category(session, category_id, page, limit)

    return json(response.to_dict())


@bp.get("/article/<id:int>")
@doc.consumes(doc.Integer(name="id"), location="path")
@doc.tag("article")
async def get_one_article(request: Request, id: int):

    session = request.ctx.session
    async with session.begin():
        response = await article_api.get_id(session, id)
        # response = await session.run_sync(article_api.get_id_sync, id)

        return json(response.to_dict())


@bp.get("/article")
@doc.tag("article")
async def get_articles(request: Request):

    page, limit = _parse_page_limit(request)

    session = request.ctx.session
    async with session.begin():
        response = await article_api.get_all(session, page, limit)

    return json(response.to_dict())


@bp.post("/articles")
@doc.tag("articles")
@doc.consumes(ArticlePost, location="body")
async def create_article(request: Request):
    json_data = request.json
    session = request.ctx.session
    art = article_api.create_from_dict(json_data)
    async with session.begin():
        session.add(art)

    return json(dict(msg="created"))


@bp.put("/article")
@doc.tag("article")
@doc.consumes(ArticlePost, location="body")
async def update_article(request: Request):
    json_data = request.json
    session = request.ctx.session
    async with session.begin():
        art = await article_api.update_article(session, json_data)

    return json(art.to_dict())


@bp.get("/category/<code:int>")
@doc.tag("category")
@doc.consumes(doc.Integer(name="code"), location="path")
@doc.produces(CategoryResponse)
async def get_categories(request: Request, code: int):
    page, limit = _parse_page_limit(request)

    session = request.ctx.session
    async with session.begin():
        response = await category_api.get_code(session, code)

        return json(response.to_dict())


@bp.get("/category")
@doc.tag("category")
@doc.produces(List[CategoryResponse])
async def get_categories(request: Request):
    page, limit = _parse_page_limit(request)

    session = request.ctx.session
    async with session.begin():
        response = await category_api.get_all(session, page, limit)

    return json(response.to_dict())


@bp.post("/category")
@doc.tag("category")
@doc.consumes(CategoryPost, location="body")
async def create_category(request: Request):
    json_data = request.json

    cat = category_api.create_from_dict(json_data)

    session = request.ctx.session
    async with session.begin():
        session.add(cat)
        # session.commit()

    return json(cat.to_dict())
