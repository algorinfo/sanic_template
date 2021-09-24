"""
The core for blog operations are here. 

For reference about how to make some query,
see:
https://docs.sqlalchemy.org/en/14/tutorial/data_select.html#tutorial-selecting-data

SQLAlchemy >= 1.4 encourage the use of select instead of query
"""

from dataclasses import dataclass
from typing import Any, Dict, List
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from changeme.blog.models import Article, Category
from changeme.blog.serializers import ArticlePost, CategoryPost
from changeme.db.utils import Pagination, get_total_async, pagination


@dataclass
class AllResponse:
    rows: List[Dict[str, Any]]
    next_page: int
    total: int

    def to_dict(self):
        return dict(rows=self.rows,
                    next_page=self.next_page,
                    total=self.total)


class ArticleApi:

    def __init__(self, rules=('-category_id',)):
        self.rules = rules

    async def get_all(self, session, page, limit) -> AllResponse:
        total = await get_total_async(session, Article)
        page = Pagination(total=total, limit=limit, page=page)
        slct = select(Article).options(selectinload(Article.category))
        stmt, next_p = pagination(slct, page)
        results = await session.execute(stmt)

        rows = [r.to_dict(rules=self.rules)
                for r in results.scalars()]

        return AllResponse(rows=rows, next_page=next_p, total=total)

    async def by_category(self, session, category_id, page, limit) -> AllResponse:
        total = await get_total_async(session, Article)
        page = Pagination(total=total, limit=limit, page=page)
        slct = select(Article)\
            .options(selectinload(Article.category))\
            .filter(Article.category_id == category_id)\
            .order_by(Article.updated_at.desc())
        stmt, next_p = pagination(slct, page)
        results = await session.execute(stmt)

        rows = [r.to_dict(rules=self.rules)
                for r in results.scalars()]

        return AllResponse(rows=rows, next_page=next_p, total=total)

    async def update_article(self, session, data: Dict[str, Any]):
        new_article = ArticlePost(**data)
        old_article = await self.get_id(session, new_article.id)
        _now = datetime.utcnow()
        old_article.updated_at = _now
        old_article.title = new_article.title
        old_article.content = new_article.content
        old_article.category_id = new_article.category_id
        session.add(old_article)

        return old_article

    async def get_id(self, session, id_) -> Article:
        stmt = select(Article).options(selectinload(Article.category))\
                              .filter(Article.id == id_)
        result = await session.execute(stmt)
        one = result.scalar()
        return one

    def get_id_sync(self, session, id_) -> Article:
        stmt = select(Article).filter(Article.id == id_)
        result = session.execute(stmt)
        one = result.fetchall()
        return one[0][0].to_dict()

    def create_from_dict(self, data: Dict[str, Any]) -> Article:
        post_data = ArticlePost(**data)
        art = Article(title=post_data.title,
                      content=post_data.content,
                      category_id=post_data.category_id)
        return art


class CategoryApi:

    def __init__(self, rules=None):
        self.rules = rules

    async def get_all(self, session, page, limit) -> AllResponse:
        total = await get_total_async(session, Category)
        page = Pagination(total=total, limit=limit, page=page)
        slct = select(Category)
        stmt, next_p = pagination(slct, page)
        results = await session.execute(stmt)

        rows = [r.to_dict()
                for r in results.scalars()]

        return AllResponse(rows=rows, next_page=next_p, total=total)

    async def get_code(self, session, code) -> Category:
        stmt = select(Category).filter(Category.code == code)
        result = await session.execute(stmt)
        one = result.scalar()
        return one

    def create_from_dict(self, data: Dict[str, Any]) -> Category:
        post_data = CategoryPost(**data)
        cat = Category(code=post_data.code,
                       description=post_data.description)

        return cat
