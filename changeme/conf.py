import logging
import os

class Config:
    SQL = os.getenv("BLOG_SQL")
    ASQL = os.getenv("BLOG_ASQL")
    CHROME = os.getenv("BLOG_CHROME")
    REDIS = os.getenv("BLOG_REDIS")
    REDIS_NS = os.getenv("BLOG_REDIS_NS", "TWT")
    QNAME = os.getenv("BLOG_QNAME")


_LOG_LEVEl = os.getenv("BLOG_LOG", "INFO")
_level = getattr(logging, _LOG_LEVEl)

logging.basicConfig(format='%(asctime)s %(message)s', level=_level)
