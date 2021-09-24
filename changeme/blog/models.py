from datetime import datetime

import pytz
from sqlalchemy import (BigInteger, Boolean, Column, DateTime, ForeignKey,
                        Integer, SmallInteger, String, Text, event)
from sqlalchemy.dialects.postgresql import JSONB
# from sqlalchemy.orm import declarative_mixin, relationship
from sqlalchemy.orm import relationship
from sqlalchemy.orm.mapper import Mapper
from sqlalchemy_serializer import SerializerMixin
from db.common import Base

# from sqlalchemy.orm import declared_attr


class Category(Base, SerializerMixin):
    # pylint: disable=too-few-public-methods
    __tablename__ = 'blog_category'

    id = Column(SmallInteger, primary_key=True)
    code = Column(SmallInteger, unique=True, nullable=False, index=True)
    description = Column(String(), nullable=False)

    # articles = relationship("Article", backref="blog_category")
    # articles = relationship("Article", backref="blog_category")
    created_at = Column(DateTime(),
                        index=True,
                        default=datetime.utcnow(),
                        nullable=False)
    # required in order to access columns with server defaults
    # or SQL expression defaults, subsequent to a flush, without
    # triggering an expired load
    __mapper_args__ = {"eager_defaults": True}


class Article(Base, SerializerMixin):
    # pylint: disable=too-few-public-methods

    __tablename__ = "blog_article"
    id = Column(BigInteger, primary_key=True)
    slug = Column(String(), unique=True, index=True, nullable=False)
    title = Column(String(), nullable=False)
    content = Column(Text(),  nullable=False)
    draft = Column(Boolean(),  default=True)
    author = Column(String())
    # tags = Column(String())

    category_id = Column(SmallInteger, ForeignKey(
        'blog_category.id', ondelete='SET NULL'),
        index=True)

    category = relationship("Category")

    # author_id = Column(Integer, ForeignKey(
    #    'blog_author.id', ondelete='SET NULL'),
    #    index=True)

    updated_at = Column(DateTime(),
                        default=datetime.utcnow(),
                        nullable=False, index=False)

    created_at = Column(DateTime(),
                        index=True,
                        default=datetime.utcnow(),
                        nullable=False)

    __mapper_args__ = {"eager_defaults": True}


# @event.listens_for(Article, 'before_update')
# def do_update_site(mapper: Mapper, connect, target: Article):
#    # pylint: disable=unused-argument
#    # target is an instance of Table
#    target.updated_at = datetime.utcnow()
